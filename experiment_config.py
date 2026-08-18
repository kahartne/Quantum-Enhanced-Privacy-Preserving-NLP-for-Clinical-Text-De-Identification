# ============================================================
# QuantumHPC Experiment Configuration
# ============================================================
# Edit this file to change experiment parameters.
# The rest of the code should not need to change.
# ============================================================


# ----------------------------
# Dataset
# ----------------------------

DATASET = "sample_clinical.csv"


# ----------------------------
# Quantum Circuit
# ----------------------------

NUM_QUBITS = 5
NUM_FEATURES = 5
FEATURE_MAP_REPS = 1


# ----------------------------
# Simulation
# ----------------------------

BACKEND = "cpu"
SHOTS = 1024


# ----------------------------
# Noise Experiment
# ----------------------------

EPSILONS = [1.0, 2.0, 4.0, 8.0]

DELTA = 1e-5

CONDITIONS = [
    "noiseless",
    "depolarizing",
    "amplitude_damping",
]


# ----------------------------
# Experiment Options
# ----------------------------

RUN_MANUAL_CIRCUIT = True
RUN_LIBRARY_CIRCUIT = True