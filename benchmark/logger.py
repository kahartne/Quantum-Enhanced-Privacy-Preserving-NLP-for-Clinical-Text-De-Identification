"""
logger.py

Utilities for logging benchmark results.
"""

from pathlib import Path
from datetime import datetime
import csv


class ExperimentLogger:
    """
    Logs experiment results to a CSV file.
    """

    def __init__(self, output_file):

        self.output_file = Path(output_file)

        self.header = [
            "Timestamp",
            "Epsilon",
            "Delta",
            "Condition",
            "Dataset",
            "Backend",
            "Qubits",
            "Features",
            "Feature_Map_Reps",
            "Shots",
            "Library_Build_ms",
            "Manual_Build_ms",
            "Simulation_ms",
        ]

        # Create file if it doesn't exist
        if not self.output_file.exists():

            with open(self.output_file, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow(self.header)

    def log(
        self,
        epsilon,
        delta,
        condition,
        dataset,
        backend,
        qubits,
        features,
        reps,
        shots,
        library_build_ms,
        manual_build_ms,
        simulation_ms,
    ):

        with open(self.output_file, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                epsilon,
                delta,
                condition,
                dataset,
                backend,
                qubits,
                features,
                reps,
                shots,
                round(library_build_ms, 3),
                round(manual_build_ms, 3),
                round(simulation_ms, 3),
            ])