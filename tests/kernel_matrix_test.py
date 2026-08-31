import numpy as np

from qiskit.quantum_info import Statevector

from circuits.feature_maps import FeatureMapBuilder


def encode(feature_vector):
    """Encode one feature vector using the manual ZZFeatureMap."""
    builder = FeatureMapBuilder(
        reps=1,
        entanglement="linear"
    )

    circuit = builder.build_manual(len(feature_vector))
    bound_circuit = circuit.assign_parameters(feature_vector)

    return Statevector.from_instruction(bound_circuit)


def kernel(state_a, state_b):
    """Calculate the quantum kernel from state overlap."""
    overlap = np.vdot(state_a.data, state_b.data)
    return abs(overlap) ** 2


def build_kernel_matrix(feature_vectors):
    """
    Build a symmetric quantum kernel matrix.

    Each feature vector is encoded exactly once.
    Only the upper triangle is calculated directly.
    """
    n = len(feature_vectors)

    states = [
        encode(feature_vector)
        for feature_vector in feature_vectors
    ]

    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            value = kernel(states[i], states[j])

            matrix[i, j] = value
            matrix[j, i] = value

    return matrix


def main():
    # Four 4-dimensional feature vectors.
    # Eddie's current implementation supports 4 features / 4 qubits.
    feature_vectors = np.array([
        [0.25, 0.50, 0.75, 1.00],
        [1.00, 0.75, 0.50, 0.25],
        [0.10, 0.30, 0.60, 0.90],
        [0.90, 0.60, 0.30, 0.10],
    ])

    kernel_matrix = build_kernel_matrix(feature_vectors)

    print("=" * 60)
    print("4x4 Quantum Kernel Matrix Test")
    print("=" * 60)

    print(f"Number of samples  : {len(feature_vectors)}")
    print(f"Feature dimension   : {feature_vectors.shape[1]}")
    print(f"Number of qubits    : {feature_vectors.shape[1]}")
    print(f"Feature-map reps    : 1")

    print("\nFeature vectors:")
    for i, vector in enumerate(feature_vectors):
        print(f"X{i} = {vector}")

    print("\nKernel matrix:")
    print("-" * 60)
    print(kernel_matrix)

    print("\nValidation")
    print("-" * 60)

    # Diagonal should be 1 because K(x, x) = 1.
    diagonal_pass = np.allclose(
        np.diag(kernel_matrix),
        1.0,
        atol=1e-10
    )

    # Quantum kernel should be symmetric.
    symmetry_pass = np.allclose(
        kernel_matrix,
        kernel_matrix.T,
        atol=1e-10
    )

    # Fidelity-based kernel values must lie in [0, 1].
    range_pass = np.all(
        (kernel_matrix >= -1e-10)
        & (kernel_matrix <= 1.0 + 1e-10)
    )

    # A valid kernel matrix should be positive semidefinite.
    eigenvalues = np.linalg.eigvalsh(kernel_matrix)
    psd_pass = np.all(eigenvalues >= -1e-10)

    print(
        f"Diagonal K(X,X) = 1      : "
        f"{'PASS' if diagonal_pass else 'FAIL'}"
    )

    print(
        f"Symmetry K(i,j)=K(j,i)   : "
        f"{'PASS' if symmetry_pass else 'FAIL'}"
    )

    print(
        f"Kernel range [0,1]       : "
        f"{'PASS' if range_pass else 'FAIL'}"
    )

    print(
        f"Positive semidefinite    : "
        f"{'PASS' if psd_pass else 'FAIL'}"
    )

    print("\nEigenvalues:")
    print(eigenvalues)

    if all([
        diagonal_pass,
        symmetry_pass,
        range_pass,
        psd_pass
    ]):
        print("\nPASS: 4x4 quantum kernel matrix is valid.")
    else:
        print("\nFAIL: Kernel matrix validation failed.")


if __name__ == "__main__":
    main()