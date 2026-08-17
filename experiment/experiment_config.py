"""
Experiment configuration for the Quantum HPC project.
"""

from dataclasses import dataclass

# --------------------------------------------------
# Supported experiment values
# --------------------------------------------------

EPSILON_VALUES = [1, 2, 4, 8]

DELTA = 1e-5

NOISE_CONDITIONS = [
    "noiseless",
    "depolarizing",
    "amplitude_damping",
]

# --------------------------------------------------
# Experiment configuration
# --------------------------------------------------

@dataclass
class ExperimentConfig:
    """
    Configuration for one QuantumHPC experiment.

    Epsilon and delta describe the differential-privacy
    experiment. The noise condition describes the quantum
    simulation/noise model.
    """

    epsilon: float = 1
    delta: float = DELTA
    condition: str = "noiseless"

    def validate(self):
        """
        Validate the experiment parameters.
        """

        if self.epsilon not in EPSILON_VALUES:
            raise ValueError(
                f"Invalid epsilon: {self.epsilon}. "
                f"Supported values: {EPSILON_VALUES}"
            )

        if self.condition not in NOISE_CONDITIONS:
            raise ValueError(
                f"Invalid condition: {self.condition}. "
                f"Supported values: {NOISE_CONDITIONS}"
            )

        if self.delta <= 0:
            raise ValueError(
                f"Delta must be greater than 0. Got: {self.delta}"
            )

        return True

    def print(self):
        """
        Print the experiment configuration.
        """

        print("\nExperiment Configuration")
        print("-" * 40)

        print(f"Epsilon   : {self.epsilon}")
        print(f"Delta     : {self.delta}")
        print(f"Condition : {self.condition}")