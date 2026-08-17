"""
config.py

Global configuration for the Quantum HPC project.
"""

from pathlib import Path
import os

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Dataset
# --------------------------------------------------

DATASET_NAME = "sample_clinical.csv"
DATASET_PATH = DATA_DIR / DATASET_NAME

# --------------------------------------------------
# Quantum Settings
# --------------------------------------------------

NUM_QUBITS = 8
FEATURE_MAP_REPS = 1
SHOTS = 1024

# --------------------------------------------------
# Backend
# --------------------------------------------------

BACKEND = "cpu"

# cpu
# gpu
# cuquantum

# ----------------------------
# Results Directories
# ----------------------------

RESULTS_DIR = PROJECT_ROOT / "results"

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

RESULTS_FILE = Path(
    os.environ.get(
        "QUANTUMHPC_RESULTS_FILE",
        LOGS_DIR / "results.csv"
    )
)

# ----------------------------
# Plot Directories
# ----------------------------

PLOTS_DIR = PROJECT_ROOT / "plots"

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