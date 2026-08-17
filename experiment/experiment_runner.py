"""
Experiment execution layer for QuantumHPC.

Coordinates dataset loading, preprocessing, feature-map
construction, quantum simulation, and result logging.
"""

import time

from config import (
    DATASET_NAME,
    DATASET_PATH,
    FEATURE_MAP_REPS,
    SHOTS,
    BACKEND,
    RESULTS_FILE,
    FEATURE_MAP_DIR,
)

import os
import csv

from benchmark.logger import ExperimentLogger
from datasets.loader import DatasetLoader
from datasets.preprocessing import DataPreprocessor
from circuits.feature_maps import FeatureMapBuilder
from simulation import QuantumSimulator
from experiment.experiment_config import ExperimentConfig

class ExperimentRunner:
    """
    Coordinates one complete QuantumHPC experiment.
    """

    def __init__(self, experiment_config=None):

        if experiment_config is None:
            experiment_config = ExperimentConfig()

        self.config = experiment_config
        self.config.validate()

    # --------------------------------------------------
    # Dataset
    # --------------------------------------------------

    def load_dataset(self):
        """
        Load the configured dataset.
        """

        loader = DatasetLoader(DATASET_PATH)

        df = loader.load()

        return loader, df

    def preprocess(self, df):
        """
        Preprocess the loaded dataset.
        """

        return DataPreprocessor(df)

    # --------------------------------------------------
    # Quantum circuit
    # --------------------------------------------------

    def build_circuits(self, processor):
        """
        Build both the library and manual feature maps.
        """

        num_features = processor.number_of_features()

        builder = FeatureMapBuilder(
            reps=FEATURE_MAP_REPS
        )

        # Library feature map
        start = time.perf_counter()

        library_circuit = builder.build(
            num_features
        )

        library_time = (
            time.perf_counter() - start
        ) * 1000

        # Manual feature map
        start = time.perf_counter()

        manual_circuit = builder.build_manual(
            num_features
        )

        manual_time = (
            time.perf_counter() - start
        ) * 1000

        return (
            builder,
            library_circuit,
            manual_circuit,
            library_time,
            manual_time,
        )

    # --------------------------------------------------
    # Simulation
    # --------------------------------------------------

    def simulate(
        self,
        simulator,
        circuit,
        feature_vector,
    ):
        """
        Run the configured quantum simulation.
        """

        counts, runtime = simulator.measurement_counts(
            circuit,
            feature_vector,
            SHOTS
        )

        return counts, runtime

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    def save_results(
        self,
        num_qubits,
        num_features,
        library_time,
        manual_time,
        simulation_time,
    ):
        """
        Log the experiment results.
        """

        logger = ExperimentLogger(
            RESULTS_FILE
        )

        logger.log(
            epsilon=self.config.epsilon,
            delta=self.config.delta,
            condition=self.config.condition,
            dataset=DATASET_NAME,
            backend=BACKEND,
            qubits=num_qubits,
            features=num_features,
            reps=FEATURE_MAP_REPS,
            shots=SHOTS,
            library_build_ms=library_time,
            manual_build_ms=manual_time,
            simulation_ms=simulation_time,
        )

    # --------------------------------------------------
    # Main execution
    # --------------------------------------------------

    def run(self):

        print("=" * 60)
        print("Quantum HPC Experiment")
        print("=" * 60)

        # ----------------------------------------------
        # Experiment configuration
        # ----------------------------------------------

        self.config.print()

        # ----------------------------------------------
        # Dataset
        # ----------------------------------------------

        loader, df = self.load_dataset()

        processor = self.preprocess(df)

        print("\nDataset")
        print("-" * 40)

        print(f"Shape: {loader.shape()}")

        print("\nColumns:")
        print(loader.columns())

        print("\nPreview:")
        print(loader.preview())

        print("\nNumeric Columns:")
        print(loader.numeric_columns())

        print("\nText Columns:")
        print(loader.text_columns())

        print("\nFeature Matrix Shape:")
        print(processor.feature_matrix().shape)

        print("\nNumber of Numeric Features:")
        print(processor.number_of_features())

        print("\nFeature Names:")
        print(processor.feature_names())

        # ----------------------------------------------
        # Feature map
        # ----------------------------------------------

        (
            builder,
            library_circuit,
            manual_circuit,
            library_time,
            manual_time,
        ) = self.build_circuits(processor)

        num_features = processor.number_of_features()
        num_qubits = manual_circuit.num_qubits

        feature_names = processor.feature_names()
        feature_matrix = processor.feature_matrix()
        feature_vector = feature_matrix[0]

        # ----------------------------------------------
        # Simulator
        # ----------------------------------------------

        simulator = QuantumSimulator(
            backend=BACKEND,
            condition=self.config.condition,
        )

        simulator.info()

        simulator.print_experiment_info(
            DATASET_NAME,
            simulator.backend_name(),
            SHOTS
        )

        simulator.print_featuremap_info(
            FEATURE_MAP_REPS,
            "linear"
        )

        simulator.print_circuit_info(
            manual_circuit,
            feature_names
        )

        simulator.print_statevector_summary(
            manual_circuit,
            feature_vector,
            feature_names
        )

        # ----------------------------------------------
        # Execute
        # ----------------------------------------------

        counts, simulation_time = self.simulate(
            simulator,
            manual_circuit,
            feature_vector
        )

        print("\nMeasurement Counts")
        print("-" * 40)

        for state, count in sorted(
            counts.items(),
            key=lambda item: item[1],
            reverse=True
        )[:10]:

            print(
                f"|{state}> : {count:>4}"
            )

        # ----------------------------------------------
        # Circuit information
        # ----------------------------------------------

        simulator.print_circuit_statistics(
            manual_circuit
        )

        simulator.print_runtime_summary(
            library_time,
            manual_time
        )

        print("\nExecution")
        print("-" * 40)

        print(
            f"Simulation Time : "
            f"{simulation_time:.3f} ms"
        )

        # ----------------------------------------------
        # Save circuits
        # ----------------------------------------------

        library_plot = (
            FEATURE_MAP_DIR /
            f"library_q{num_qubits}_r{FEATURE_MAP_REPS}.png"
        )

        builder.save(
            library_circuit.decompose(),
            library_plot
        )

        manual_plot = (
            FEATURE_MAP_DIR /
            f"manual_q{num_qubits}_r{FEATURE_MAP_REPS}.png"
        )

        builder.save(
            manual_circuit,
            manual_plot
        )

        print(
            f"\nLibrary circuit saved to: "
            f"{library_plot}"
        )

        print(
            f"Manual circuit saved to: "
            f"{manual_plot}"
        )

        # ----------------------------------------------
        # Log
        # ----------------------------------------------

        self.save_results(
            num_qubits,
            num_features,
            library_time,
            manual_time,
            simulation_time,
        )

        print(
            f"\nResults saved to: "
            f"{RESULTS_FILE}"
        )

        print("\nComplete!")

        return {
            "dataset": DATASET_NAME,
            "epsilon": self.config.epsilon,
            "delta": self.config.delta,
            "condition": self.config.condition,
            "backend": BACKEND,
            "qubits": num_qubits,
            "features": num_features,
            "library_build_time": library_time,
            "manual_build_time": manual_time,
            "simulation_time": simulation_time,
        }