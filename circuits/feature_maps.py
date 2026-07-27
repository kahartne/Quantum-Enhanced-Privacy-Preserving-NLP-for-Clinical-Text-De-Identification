"""
feature_maps.py

Quantum feature map utilities.
"""

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import ZZFeatureMap
from qiskit.visualization import circuit_drawer
import numpy as np


class FeatureMapBuilder:
    """
    Builds quantum feature maps for encoding classical data.
    """

    def __init__(self,
                 reps=2,
                 entanglement="linear"):

        self.reps = reps
        self.entanglement = entanglement

    def build(self,
              num_features):

        feature_map = ZZFeatureMap(
            feature_dimension=num_features,
            reps=self.reps,
            entanglement=self.entanglement
        )

        return feature_map
    
    def build_manual(self, num_features):
        """
        Build a ZZFeatureMap manually using primitive gates.
        """

        qc = QuantumCircuit(num_features)

        x = ParameterVector("x", num_features)

        for _ in range(self.reps):

            # -------------------------------------------------
            # Hadamard layer
            # -------------------------------------------------

            for qubit in range(num_features):
                qc.h(qubit)

            # -------------------------------------------------
            # Feature encoding
            # -------------------------------------------------

            for qubit in range(num_features):
                qc.p(2 * x[qubit], qubit)

            # -------------------------------------------------
            # ZZ entanglement
            # -------------------------------------------------

            for qubit in range(num_features - 1):

                qc.cx(qubit, qubit + 1)

                qc.p(
                    2 * (np.pi - x[qubit])
                    * (np.pi - x[qubit + 1]),
                    qubit + 1
                )

                qc.cx(qubit, qubit + 1)

        return qc
    
    def save(self, circuit, filename):
        """
        Save a circuit diagram as a PNG image.
        """

        circuit_drawer(
            circuit,
            output="mpl",
            filename=str(filename)
        )