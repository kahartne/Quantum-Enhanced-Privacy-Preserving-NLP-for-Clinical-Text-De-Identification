"""
Global configuration for the Quantum HPC project.

This file contains the default settings for experiments.
Edit the values in the sections below to change the default
experiment configuration.
"""

from pathlib import Path
import os


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
PLOTS_DIR = PROJECT_ROOT / "plots"


# ============================================================
# Dataset
# ============================================================

DATASET_NAME = "sample_clinical.csv"
DATASET_PATH = DATA_DIR / DATASET_NAME


# ============================================================
# Quantum Circuit
# ============================================================

# NOTE:
# NUM_QUBITS is currently reserved for the future circuit
# configuration. The current feature-map implementation
# derives the number of qubits from the number of features.
NUM_QUBITS = 8

FEATURE_MAP_REPS = 1


# ============================================================
# Simulation
# ============================================================

SHOTS = 1024

BACKEND = "cpu"

# Available backend options:
#   cpu
#   gpu
#   cuquantum


# ============================================================
# Privacy / Noise Experiment
# ============================================================

DEFAULT_EPSILON = 1.0

DELTA = 1e-5

DEFAULT_CONDITION = "noiseless"

EPSILON_VALUES = [
    1.0,
    2.0,
    4.0,
    8.0,
]

NOISE_CONDITIONS = [
    "noiseless",
    "depolarizing",
    "amplitude_damping",
]


# ============================================================
# Results
# ============================================================

LOGS_DIR = RESULTS_DIR / "logs"
TABLES_DIR = RESULTS_DIR / "tables"
EXPORTS_DIR = RESULTS_DIR / "exports"

for directory in [
    RESULTS_DIR,
    LOGS_DIR,
    TABLES_DIR,
    EXPORTS_DIR,
]:
    directory.mkdir(exist_ok=True)


# Main results file.
#
# QUANTUMHPC_RESULTS_FILE can be set by SLURM or another
# external process to override this location.
RESULTS_FILE = Path(
    os.environ.get(
        "QUANTUMHPC_RESULTS_FILE",
        LOGS_DIR / "results.csv"
    )
)


# ============================================================
# Plot Directories
# ============================================================

FEATURE_MAP_DIR = PLOTS_DIR / "feature_maps"
CIRCUIT_DIR = PLOTS_DIR / "circuits"
RUNTIME_DIR = PLOTS_DIR / "runtime"
THROUGHPUT_DIR = PLOTS_DIR / "throughput"
SCALING_DIR = PLOTS_DIR / "scaling"
COMPARISON_DIR = PLOTS_DIR / "comparisons"

for directory in [
    PLOTS_DIR,
    FEATURE_MAP_DIR,
    CIRCUIT_DIR,
    RUNTIME_DIR,
    THROUGHPUT_DIR,
    SCALING_DIR,
    COMPARISON_DIR,
]:
    directory.mkdir(exist_ok=True)