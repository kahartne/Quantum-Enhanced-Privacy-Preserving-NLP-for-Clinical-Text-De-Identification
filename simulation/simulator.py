"""
Quantum simulation backend.

Provides helper functions for running quantum circuits
using Qiskit Aer.
"""
import numpy as np
import time
from backends.backend_factory import BackendFactory
from experiment.aer_noise_factory import NoiseModelFactory
from qiskit.quantum_info import Statevector
from qiskit import transpile

class QuantumSimulator:
    """
    Runs quantum circuits using Qiskit Aer.
    """

    def __init__(
        self,
        backend="cpu",
        condition="noiseless",
    ):
        self.backend_type = backend.lower()
        self.condition = condition.lower()

        self.noise_model = NoiseModelFactory.create(
            condition=self.condition
        )

        self.backend = BackendFactory.create(
            self.backend_type
        )

    def backend_name(self):

        return self.backend_type
    
    """
    Execution
    """
    
    def execute(self, circuit, feature_vector, shots=1024):
        """
        Execute a quantum circuit.
        """

        bound = circuit.assign_parameters(feature_vector)

        measured = bound.copy()
        measured.measure_all()

        compiled = transpile(measured, self.backend)

        start = time.perf_counter()

        job = self.backend.run(compiled, shots=shots, noise_model=self.noise_model)

        result = job.result()

        runtime = (time.perf_counter() - start) * 1000

        return result, runtime
    
    def statevector(self, circuit, feature_vector):
        """
        Return the statevector after binding feature values.
        """

        bound_circuit = circuit.assign_parameters(feature_vector)

        return Statevector.from_instruction(bound_circuit)
    
    def measurement_counts(self, circuit, feature_vector, shots=1024):

        result, runtime = self.execute(circuit, feature_vector, shots)
        counts = result.get_counts()

        return counts, runtime
    
    """
    Printing
    """
    def info(self):

        print("\nSimulation Backend")
        print("-" * 40)

        print(f"Backend : {self.backend_type}")
        print(f"Aer     : {self.backend.name}")

        try:
            print(f"Method  : {self.backend.options.method}")
        except Exception:
            pass

        try:
            print(f"Device  : {self.backend.options.device}")
        except Exception:
            pass

        print(f"Noise   : {self.condition}")
    
    def print_runtime_summary(self, library_build_time, manual_build_time):

        print("\nRuntime Summary")
        print("-" * 40)

        print(f"Library Build : {library_build_time:.3f} ms")
        print(f"Manual Build  : {manual_build_time:.3f} ms")
    
    def print_experiment_info(self, dataset, backend, shots):
        """
        Print experiment configuration.
        """

        print("\nExperiment")
        print("-" * 40)

        print(f"Dataset : {dataset}")
        print(f"Backend : {backend}")
        print(f"Shots   : {shots}")
    
    def print_featuremap_info(self, reps, entanglement):
        print("\nZZFeatureMap Configuration")
        print("-" * 40)

        print(f"Repetitions  : {reps}")
        print(f"Entanglement : {entanglement}")
    
    def print_circuit_info(self, circuit, feature_names):
        print("\nCircuit Metadata")
        print("-" * 40)

        print(f"Circuit Type      : Manual ZZFeatureMap")
        print(f"Circuit Name      : {circuit.name}")
        print(f"Qubits            : {circuit.num_qubits}")
        print(f"Depth             : {circuit.depth()}")
        print(f"Width             : {circuit.width()}")

        params = list(circuit.parameters)
        print()
        print(f"Parameters      : {len(params)}")

        if params:
            names = ", ".join(str(p) for p in params[:5])

            if len(params) > 5:
                names += ", ..."

            print(f"Parameter Names : {names}")

        print(f"Parameterized   : {'Yes' if params else 'No'}")

        print("\nFeature Encoding")
        print("-" * 40)

        print(f"Clinical Features : {len(feature_names)}")
        print(f"Quantum Qubits    : {circuit.num_qubits}")
        print()
        print(f"{'Feature':<22}{'Qubit'}")
        print("-" * 30)

        for i, name in enumerate(feature_names):
            print(f"{name:<22}q{i}")
    
    def print_statevector_summary(self, circuit, feature_vector, feature_names):

        state = self.statevector(
            circuit,
            feature_vector
        )

        probabilities = np.abs(state.data) ** 2
        phases = np.angle(state.data)

        print("\nFeature Vector")
        print("-" * 40)

        for name, value in zip(feature_names, feature_vector):
            print(f"{name:<16}: {value}")

        print("\nQuantum State Summary")
        print("-" * 40)

        print(f"Qubits          : {circuit.num_qubits}")
        print(f"State Dimension : {len(state.data)}")
        print(f"Normalization   : {probabilities.sum():.6f}")

        print("\nBound Statevector")
        print("-" * 40)

        print(
            f"{'State':<10}"
            f"{'Probability':<15}"
            f"{'Phase(rad)':<12}"
        )

        for index in range(min(10, len(probabilities))):

            bitstring = format(
                index,
                f"0{circuit.num_qubits}b"
            )

            print(
                f"|{bitstring}>"
                f"{probabilities[index]:>13.6f}"
                f"{phases[index]:>15.3f}"
            )
    
    def print_counts(self, circuit, feature_vector, shots=1024):

        counts, runtime = self.measurement_counts(circuit, feature_vector, shots)

        print("\nMeasurement Counts")
        print("-" * 40)

        print(f"{'State':<10}{'Counts'}")
        print("-" * 25)

        for state, count in sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]:

            print(f"|{state}> : {count:>4}")
        
        print("\nExecution")
        print("-" * 40)

        print(f"Shots          : {shots}")
        print(f"Unique States  : {len(counts)}")
        print(f"Execution Time : {runtime:.3f} ms")
        
        avg_time = runtime / shots
        print(f"Avg / Shot     : {avg_time:.6f} ms")
    
    def print_circuit_statistics(self, circuit):
        """
        Print useful statistics about a quantum circuit.
        """

        print("\nCircuit Statistics")
        print("-" * 40)

        print(f"Qubits          : {circuit.num_qubits}")
        print(f"Classical Bits  : {circuit.num_clbits}")
        print()
        print(f"Depth           : {circuit.depth()}")
        print(f"Width           : {circuit.width()}")
        print()
        print(f"Parameters      : {len(circuit.parameters)}")
        print(f"Total Gates     : {len(circuit.data)}")

        print("\nGate Breakdown")
        print("-" * 40)

        gate_counts = dict(sorted(circuit.count_ops().items()))

        for gate, count in sorted(gate_counts.items()):
            print(f"{gate:<12}{count:>4}")