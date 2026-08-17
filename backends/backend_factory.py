"""
Backend factory for QuantumHPC.

Creates Qiskit Aer simulator backends based on the
requested execution device.
"""

from qiskit_aer import AerSimulator

class BackendFactory:
    """
    Factory for creating QuantumHPC simulation backends.
    """

    SUPPORTED_BACKENDS = {
        "cpu",
        "gpu",
        "cuquantum",
    }

    @staticmethod
    def create(
        backend="cpu",
        method="automatic",
    ):
        """
        Create and return an AerSimulator configured for
        the requested backend.

        Parameters
        ----------
        backend : str
            Requested execution backend:
            "cpu", "gpu", or "cuquantum".

        method : str
            Aer simulation method. Defaults to "automatic".

        Returns
        -------
        AerSimulator
            Configured Qiskit Aer simulator.

        Raises
        ------
        ValueError
            If an unsupported backend is requested.
        """

        backend = backend.lower()

        if backend not in BackendFactory.SUPPORTED_BACKENDS:
            raise ValueError(
                f"Unsupported backend: '{backend}'. "
                f"Supported backends: "
                f"{sorted(BackendFactory.SUPPORTED_BACKENDS)}"
            )

        # --------------------------------------------------
        # CPU
        # --------------------------------------------------

        if backend == "cpu":
            return AerSimulator(
                method=method,
                device="CPU",
            )

        # --------------------------------------------------
        # GPU
        # --------------------------------------------------

        if backend == "gpu":
            return AerSimulator(
                method=method,
                device="GPU",
            )

        # --------------------------------------------------
        # cuQuantum
        # --------------------------------------------------

        if backend == "cuquantum":
            return AerSimulator(
                method="tensor_network",
                device="GPU",
            )

        # This should never be reached because of the
        # validation above.
        raise ValueError(
            f"Unable to create backend: {backend}"
        )