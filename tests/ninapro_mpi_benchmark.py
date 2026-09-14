"""
NinaPro DB2 MPI quantum-kernel benchmark.

This benchmark applies MPI to the project's real NinaPro workload:

    NinaPro DB2
        -> 102 x 8 quantum features
        -> manual ZZFeatureMap state encoding
        -> symmetric 102 x 102 quantum-kernel matrix

Each feature vector is encoded exactly once per run. Encoded states are
shared across MPI ranks, and the unique upper-triangular kernel-pair
calculations are divided evenly across ranks. The lower triangle is then
reconstructed from symmetry on rank 0.

This measures MPI workload parallelism for quantum-kernel evaluation; it
is not distributed quantum-statevector simulation.
"""

import argparse
import csv
import os
import time
from datetime import datetime

import numpy as np
from mpi4py import MPI

from datasets.ninapro import NinaProProcessor
from simulation.quantum_kernel import QuantumKernel


DEFAULT_DATASET = "data/ninapro/DB2/s1/S1_E1_A1.mat"
DEFAULT_RESULTS = "results/logs/ninapro_mpi_scaling.csv"


def split_work(total_items, rank, size):
    """Return the [start, end) slice assigned to one MPI rank."""

    base = total_items // size
    remainder = total_items % size

    start = rank * base + min(rank, remainder)
    end = start + base

    if rank < remainder:
        end += 1

    return start, end


def build_upper_triangle_pairs(n_samples):
    """Return all unique (i, j) pairs for i <= j."""

    return [
        (i, j)
        for i in range(n_samples)
        for j in range(i, n_samples)
    ]


def evaluate_state_pair(state_a, state_b):
    """Evaluate K(a,b) directly from two complex state arrays."""

    overlap = np.vdot(state_a, state_b)
    return float(abs(overlap) ** 2)


def validate_kernel_matrix(kernel_matrix, expected_size):
    """Validate the reconstructed symmetric kernel matrix."""

    if kernel_matrix.shape != (expected_size, expected_size):
        raise ValueError(
            f"Unexpected kernel shape: {kernel_matrix.shape}"
        )

    if not np.all(np.isfinite(kernel_matrix)):
        raise ValueError("Kernel matrix contains non-finite values")

    if not np.allclose(
        kernel_matrix,
        kernel_matrix.T,
        atol=1e-6,
    ):
        raise ValueError("Kernel matrix is not symmetric")

    if not np.allclose(
        np.diag(kernel_matrix),
        1.0,
        atol=1e-5,
    ):
        raise ValueError("Kernel matrix diagonal is not approximately 1")

    if np.min(kernel_matrix) < -1e-6 or np.max(kernel_matrix) > 1.0 + 1e-6:
        raise ValueError("Kernel values fall outside the expected [0, 1] range")


def run_once(comm, kernel, feature_matrix, pair_indices):
    """
    Run one complete distributed kernel-matrix evaluation.

    The timed region includes:
      1. local state encoding,
      2. all-rank state exchange,
      3. distributed upper-triangle pair evaluation,
      4. gathering pair values to rank 0.

    Dataset preprocessing is intentionally outside the timed region, matching
    the local NinaPro benchmark's treatment of preprocessing as setup.
    """

    rank = comm.Get_rank()
    size = comm.Get_size()

    sample_start, sample_end = split_work(
        len(feature_matrix),
        rank,
        size,
    )

    pair_start, pair_end = split_work(
        len(pair_indices),
        rank,
        size,
    )

    comm.Barrier()
    start = MPI.Wtime()

    # Encode each feature vector exactly once across the MPI ranks.
    local_states = [
        kernel.encode(feature_vector).data
        for feature_vector in feature_matrix[sample_start:sample_end]
    ]

    # Every rank needs the complete state list for its assigned pair work.
    gathered_states = comm.allgather(local_states)
    states = np.concatenate(gathered_states, axis=0)

    # Compute only the unique upper triangle assigned to this rank.
    local_values = np.asarray(
        [
            evaluate_state_pair(states[i], states[j])
            for i, j in pair_indices[pair_start:pair_end]
        ],
        dtype=np.float64,
    )

    gathered_values = comm.gather(local_values, root=0)

    comm.Barrier()
    end = MPI.Wtime()

    wall_time_ms = (end - start) * 1000.0

    if rank != 0:
        return wall_time_ms, None

    # Pair slices were assigned contiguously by rank, so concatenation restores
    # the original pair order.
    values = np.concatenate(gathered_values, axis=0)

    kernel_matrix = np.zeros(
        (len(feature_matrix), len(feature_matrix)),
        dtype=np.float64,
    )

    for (i, j), value in zip(pair_indices, values):
        kernel_matrix[i, j] = value
        kernel_matrix[j, i] = value

    return wall_time_ms, kernel_matrix


def main():
    parser = argparse.ArgumentParser(
        description="MPI benchmark for the real NinaPro quantum-kernel workload."
    )

    parser.add_argument(
        "--file",
        default=DEFAULT_DATASET,
        help=f"NinaPro DB2 MATLAB file (default: {DEFAULT_DATASET})",
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of timed runs after one warm-up (default: 3).",
    )

    parser.add_argument(
        "--results-file",
        default=DEFAULT_RESULTS,
        help=f"CSV output path (default: {DEFAULT_RESULTS})",
    )

    args = parser.parse_args()

    if args.runs < 1:
        parser.error("--runs must be at least 1")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # ------------------------------------------------------------
    # NinaPro preprocessing is setup, not part of kernel timing.
    # Rank 0 loads the MATLAB file, then broadcasts the 102 x 8 data.
    # ------------------------------------------------------------

    if rank == 0:
        processor = NinaProProcessor(args.file)
        feature_matrix, labels, metadata = processor.process()

        feature_matrix = np.asarray(
            feature_matrix,
            dtype=np.float64,
        )
        labels = np.asarray(labels, dtype=np.int64)

        if feature_matrix.shape != (102, 8):
            raise ValueError(
                "Expected the final NinaPro benchmark workload to have "
                f"shape (102, 8), got {feature_matrix.shape}"
            )

        if len(labels) != 102 or len(metadata) != 102:
            raise ValueError("Expected exactly 102 NinaPro samples")
    else:
        feature_matrix = None
        labels = None

    feature_matrix = comm.bcast(feature_matrix, root=0)

    # The labels are not used in the kernel calculation, but broadcasting them
    # keeps the dataset metadata available on every rank if needed for checks.
    labels = comm.bcast(labels, root=0)

    n_samples, n_features = feature_matrix.shape
    pair_indices = build_upper_triangle_pairs(n_samples)

    kernel = QuantumKernel(
        reps=1,
        entanglement="linear",
        backend="cpu",
    )

    # ------------------------------------------------------------
    # Warm-up: initialize the simulator path and exercise the full workload.
    # ------------------------------------------------------------

    warmup_time, warmup_matrix = run_once(
        comm,
        kernel,
        feature_matrix,
        pair_indices,
    )

    if rank == 0:
        validate_kernel_matrix(warmup_matrix, n_samples)

    comm.Barrier()

    # ------------------------------------------------------------
    # Timed runs
    # ------------------------------------------------------------

    timed_results = []

    for run_index in range(1, args.runs + 1):
        wall_time_ms, kernel_matrix = run_once(
            comm,
            kernel,
            feature_matrix,
            pair_indices,
        )

        if rank == 0:
            validate_kernel_matrix(kernel_matrix, n_samples)

        timed_results.append(wall_time_ms)

    # ------------------------------------------------------------
    # Rank 0 reports and records the benchmark.
    # ------------------------------------------------------------

    if rank == 0:
        mean_ms = float(np.mean(timed_results))
        std_ms = float(np.std(timed_results, ddof=1)) if len(timed_results) > 1 else 0.0
        median_ms = float(np.median(timed_results))

        timestamp = datetime.now().isoformat(timespec="seconds")

        results_dir = os.path.dirname(args.results_file)
        if results_dir:
            os.makedirs(results_dir, exist_ok=True)

        file_exists = os.path.exists(args.results_file)

        with open(args.results_file, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)

            if not file_exists:
                writer.writerow([
                    "timestamp",
                    "processes",
                    "samples",
                    "features",
                    "qubits",
                    "unique_pairs",
                    "run",
                    "wall_time_ms",
                    "mean_wall_time_ms",
                    "std_wall_time_ms",
                    "median_wall_time_ms",
                    "backend",
                    "condition",
                ])

            for run_index, wall_time_ms in enumerate(timed_results, start=1):
                writer.writerow([
                    timestamp,
                    size,
                    n_samples,
                    n_features,
                    n_features,
                    len(pair_indices),
                    run_index,
                    round(wall_time_ms, 6),
                    round(mean_ms, 6),
                    round(std_ms, 6),
                    round(median_ms, 6),
                    "cpu",
                    "noiseless",
                ])

        print("=" * 68)
        print("NinaPro DB2 MPI Quantum-Kernel Benchmark")
        print("=" * 68)
        print(f"Dataset        : {args.file}")
        print(f"MPI processes  : {size}")
        print(f"Samples        : {n_samples}")
        print(f"Features       : {n_features}")
        print(f"Qubits         : {n_features}")
        print(f"Unique pairs   : {len(pair_indices)}")
        print(f"Timed runs     : {args.runs}")
        print("Backend        : cpu")
        print("Condition      : noiseless")
        print(f"Warm-up        : {warmup_time:.3f} ms")
        print("\nTimed runs")
        print("-" * 68)

        for run_index, wall_time_ms in enumerate(timed_results, start=1):
            print(f"Run {run_index}: {wall_time_ms:.3f} ms")

        print("\nSummary")
        print("-" * 68)
        print(f"Mean           : {mean_ms:.3f} ms")
        print(f"Std. deviation : {std_ms:.3f} ms")
        print(f"Median         : {median_ms:.3f} ms")
        print("Validation     : PASS")
        print(f"Results        : {args.results_file}")
        print("\nComplete.")


if __name__ == "__main__":
    main()
