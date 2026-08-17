"""
Aer quantum noise factory.

This module creates Qiskit Aer noise models for the
quantum-simulation noise-condition experiments.

Note:
    This is NOT differential privacy noise.
    Differential privacy parameters (epsilon and delta)
    are managed separately by experiment_config.py.
"""

from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    amplitude_damping_error,
)


class NoiseModelFactory:
    """
    Creates Qiskit Aer noise models.

    Supported conditions:
        - noiseless
        - depolarizing
        - amplitude_damping
    """

    SUPPORTED_CONDITIONS = {
        "noiseless",
        "depolarizing",
        "amplitude_damping",
    }

    @staticmethod
    def create(
        condition="noiseless",
        noise_strength=0.01,
    ):
        """
        Create an Aer noise model.

        Parameters
        ----------
        condition : str
            Quantum simulation noise condition.

        noise_strength : float
            Probability/strength of the quantum noise model.
            This is intentionally separate from DP epsilon.

        Returns
        -------
        NoiseModel or None
            None for noiseless simulation.
        """

        condition = condition.lower()

        if condition not in NoiseModelFactory.SUPPORTED_CONDITIONS:
            raise ValueError(
                f"Unsupported noise condition: '{condition}'. "
                f"Supported conditions: "
                f"{sorted(NoiseModelFactory.SUPPORTED_CONDITIONS)}"
            )

        if not 0.0 <= noise_strength <= 1.0:
            raise ValueError(
                "noise_strength must be between 0 and 1."
            )

        # --------------------------------------------------
        # Noiseless
        # --------------------------------------------------

        if condition == "noiseless":
            return None

        noise_model = NoiseModel()

        # The current manual ZZFeatureMap uses:
        # h, p, and cx gates.
        single_qubit_gates = [
            "h",
            "p",
        ]

        # --------------------------------------------------
        # Depolarizing noise
        # --------------------------------------------------

        if condition == "depolarizing":

            single_qubit_error = depolarizing_error(
                noise_strength,
                1,
            )

            two_qubit_error = depolarizing_error(
                noise_strength,
                2,
            )

            noise_model.add_all_qubit_quantum_error(
                single_qubit_error,
                single_qubit_gates,
            )

            noise_model.add_all_qubit_quantum_error(
                two_qubit_error,
                ["cx"],
            )

            return noise_model

        # --------------------------------------------------
        # Amplitude damping
        # --------------------------------------------------

        if condition == "amplitude_damping":

            single_qubit_error = amplitude_damping_error(
                noise_strength
            )

            noise_model.add_all_qubit_quantum_error(
                single_qubit_error,
                single_qubit_gates,
            )

            return noise_model

        raise ValueError(
            f"Unable to create noise model: {condition}"
        )