"""
MPI quantum simulation benchmark prototype.

Distributes independent quantum simulation workloads
across MPI ranks.

This is a prototype for the future quantum-kernel
MPI benchmark. The current workload uses the existing
QuantumHPC sample clinical dataset.
"""

import argparse
import time
import csv
from datetime import datetime
import numpy as np
from mpi4py import MPI

from config import (
    DATASET_NAME,
    DATASET_PATH,
    FEATURE_MAP_REPS,
    SHOTS,
    BACKEND,
)

from datasets.loader import DatasetLoader
from datasets.preprocessing import DataPreprocessor
from circuits.feature_maps import FeatureMapBuilder
from simulation import QuantumSimulator


def split_work(total_items, rank, size):
    """
    Return the start/end indices assigned to this MPI rank.

    The workload is divided as evenly as possible.
    """

    base = total_items // size
    remainder = total_items % size

    start = rank * base + min(rank, remainder)
    end = start + base

    if rank < remainder:
        end += 1

    return start, end


def main():

    # --------------------------------------------------------
    # Command-line arguments
    # --------------------------------------------------------

    parser = argparse.ArgumentParser(
        description="QuantumHPC MPI benchmark."
    )

    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Number of times to repeat the dataset for benchmarking."
    )

    args = parser.parse_args()

    if args.repeats < 1:
        parser.error("--repeats must be at least 1")

    output_path = "results/logs/mpi_scaling.csv"

    # --------------------------------------------------------
    # MPI initialization
    # --------------------------------------------------------

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()
    size = comm.Get_size()

    # --------------------------------------------------------
    # Load and preprocess dataset
    # --------------------------------------------------------

    loader = DatasetLoader(DATASET_PATH)
    df = loader.load()

    processor = DataPreprocessor(df)

    feature_matrix = processor.feature_matrix()

    if args.repeats > 1:
        feature_matrix = np.tile(
            feature_matrix,
            (args.repeats, 1),
        )

    total_samples = len(feature_matrix)

    # --------------------------------------------------------
    # Build the same manual feature map used by ExperimentRunner
    # --------------------------------------------------------

    num_features = processor.number_of_features()

    builder = FeatureMapBuilder(
        reps=FEATURE_MAP_REPS
    )

    manual_circuit = builder.build_manual(
        num_features
    )

    # --------------------------------------------------------
    # Create simulator
    # --------------------------------------------------------

    simulator = QuantumSimulator(
        backend=BACKEND,
        condition="noiseless",
    )

    # --------------------------------------------------------
    # Determine workload for this rank
    # --------------------------------------------------------

    start_index, end_index = split_work(
        total_samples,
        rank,
        size,
    )

    local_samples = feature_matrix[
        start_index:end_index
    ]

    # --------------------------------------------------------
    # Synchronize before timing
    # --------------------------------------------------------

    comm.Barrier()

    global_start = MPI.Wtime()

    local_times = []

    for feature_vector in local_samples:

        _, runtime = simulator.measurement_counts(
            manual_circuit,
            feature_vector,
            SHOTS,
        )

        local_times.append(runtime)

    comm.Barrier()

    global_end = MPI.Wtime()

    local_wall_time = (
        global_end - global_start
    ) * 1000

    # --------------------------------------------------------
    # Gather timing information
    # --------------------------------------------------------

    timing_data = comm.gather(
        {
            "rank": rank,
            "samples": len(local_samples),
            "simulation_time_ms": sum(local_times),
            "wall_time_ms": local_wall_time,
        },
        root=0,
    )

    # --------------------------------------------------------
    # Rank 0 reports results
    # --------------------------------------------------------

    if rank == 0:

        total_wall_time = max(
            item["wall_time_ms"]
            for item in timing_data
        )

        total_simulation_time = sum(
            item["simulation_time_ms"]
            for item in timing_data
        )

        # Save Benchmark Result
        timestamp = datetime.now().isoformat(timespec="seconds")

        file_exists = False

        try:
            with open(output_path, "r"):
                file_exists = True
        except FileNotFoundError:
            pass

        with open(output_path, "a", newline="") as csv_file:

            writer = csv.writer(csv_file)

            if not file_exists:
                writer.writerow([
                    "timestamp",
                    "processes",
                    "samples",
                    "repeats",
                    "features",
                    "qubits",
                    "shots",
                    "backend",
                    "condition",
                    "wall_time_ms",
                    "simulation_time_ms",
                ])

            writer.writerow([
                timestamp,
                size,
                total_samples,
                args.repeats,
                num_features,
                manual_circuit.num_qubits,
                SHOTS,
                BACKEND,
                "noiseless",
                round(total_wall_time, 3),
                round(total_simulation_time, 3),
            ])

        print("=" * 60)
        print("QuantumHPC MPI Benchmark Prototype")
        print("=" * 60)

        print(f"MPI Processes : {size}")
        print(f"Dataset       : {DATASET_NAME}")
        print(f"Samples       : {total_samples}")
        print(f"Repeats       : {args.repeats}")
        print(f"Features      : {num_features}")
        print(f"Qubits        : {manual_circuit.num_qubits}")
        print(f"Shots         : {SHOTS}")
        print(f"Backend       : {BACKEND}")
        print(f"Condition     : noiseless")

        print("\nWork Distribution")
        print("-" * 60)

        for item in timing_data:

            print(
                f"Rank {item['rank']:>2}: "
                f"{item['samples']:>3} samples | "
                f"{item['wall_time_ms']:>10.3f} ms"
            )

        print("\nBenchmark")
        print("-" * 60)

        print(
            f"Total simulation time : "
            f"{total_simulation_time:.3f} ms"
        )

        print(
            f"Total wall time       : "
            f"{total_wall_time:.3f} ms"
        )

        print("\nComplete.")


if __name__ == "__main__":
    main()