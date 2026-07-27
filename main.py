"""
main.py

Quantum HPC
Phase 1 - Dataset Framework
"""

from platform import processor
from venv import logger

from config import *

import time
from benchmark.logger import ExperimentLogger

from datasets.loader import DatasetLoader
from datasets.preprocessing import DataPreprocessor

from circuits.feature_maps import FeatureMapBuilder
from qiskit.visualization import circuit_drawer

from simulation import QuantumSimulator


def main():
    """
    Main entry point for the Quantum HPC framework.
    """

    print("=" * 60)
    print("Quantum HPC Framework")
    print("=" * 60)

    #
    # Load Dataset
    #
    loader = DatasetLoader(DATASET_PATH)

    df = loader.load()

    #
    # Preprocess Dataset
    #
    processor = DataPreprocessor(df)

    #
    # Display Dataset Information
    #
    print("\nDataset")
    print("-" * 40)

    print(f"Shape: {loader.shape()}")

    print("\nColumns:")
    print(loader.columns())

    print("\nPreview:")
    print(loader.preview())

    print("\nDataset Information:")
    loader.info()

    print("\nNumeric Columns:")
    print(loader.numeric_columns())

    print("\nText Columns:")
    print(loader.text_columns())

    #
    # Display Feature Information
    #
    print("\nFeature Matrix Shape:")
    print(processor.feature_matrix().shape)

    print("\nNumber of Numeric Features:")
    print(processor.number_of_features())

    print("\nFeature Names:")
    print(processor.feature_names())

    #
    # Quantum Feature Map / Circuit
    #
    
    num_features = processor.number_of_features()
    feature_names = processor.feature_names()

    feature_matrix = processor.feature_matrix()
    feature_vector = feature_matrix[0]

    builder = FeatureMapBuilder(
        reps=FEATURE_MAP_REPS
    )

    # Library Circuit
    start = time.perf_counter()

    library_circuit = builder.build(
        num_features
    )

    library_time = (time.perf_counter() - start) * 1000

    # Actual number of qubits in circuit
    num_qubits = library_circuit.num_qubits

    # Manual (Gate-by-Gate) Circuit
    start = time.perf_counter()

    manual_circuit = builder.build_manual(
        num_features
    )

    manual_time = (time.perf_counter() - start) * 1000

    #
    # Quantum Simulator
    #

    simulator = QuantumSimulator()

    simulator.info()
    
    simulator.print_experiment_info(DATASET_NAME, simulator.backend_name(), SHOTS)
    
    simulator.print_featuremap_info(FEATURE_MAP_REPS, "linear")
    
    simulator.print_circuit_info(manual_circuit, feature_names)
    
    simulator.print_statevector_summary(manual_circuit, feature_vector, feature_names)
    
    simulator.print_counts(manual_circuit, feature_vector, SHOTS)
    
    simulator.print_circuit_statistics(manual_circuit)

    simulator.print_runtime_summary(library_time, manual_time)

    #
    # Print Circuits
    #
    
    print("\nLibrary Feature Map")
    print("-" * 40)

    print(library_circuit)

    print("\nLibrary Decomposed Circuit")
    print("-" * 40)

    print(library_circuit.decompose())

    print("\nManual Circuit")
    print("-" * 40)

    print(manual_circuit)

    #
    # Save library circuit
    #

    library_plot = (
        FEATURE_MAP_DIR /
        f"library_q{num_qubits}_r{FEATURE_MAP_REPS}.png"
    )

    builder.save(
        library_circuit.decompose(),
        library_plot
    )

    print(f"\nLibrary circuit saved to: {library_plot}")

    #
    # Save manual circuit
    #

    manual_plot = (
        FEATURE_MAP_DIR /
        f"manual_q{num_qubits}_r{FEATURE_MAP_REPS}.png"
    )

    builder.save(
        manual_circuit,
        manual_plot
    )

    print(f"Manual circuit saved to: {manual_plot}")

    #
    # Log Results
    #

    logger = ExperimentLogger(RESULTS_FILE)

    logger.log(
        dataset=DATASET_NAME,
        backend=BACKEND,
        qubits=num_qubits,
        features=num_features,
        reps=FEATURE_MAP_REPS,
        shots=SHOTS,
        runtime=library_time
    )

    print(f"\nLibrary Build Time: {library_time:.3f} ms")
    print(f"Manual Build Time:  {manual_time:.3f} ms")
    print(f"Results saved to: {RESULTS_FILE}")

    print("\nComplete!")


if __name__ == "__main__":
    main()