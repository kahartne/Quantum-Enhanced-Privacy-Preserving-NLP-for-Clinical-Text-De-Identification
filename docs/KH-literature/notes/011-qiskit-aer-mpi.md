# 011 – Qiskit Aer MPI and Distributed Simulation

## IEEE Reference

[11] Qiskit Development Team, "Qiskit Aer Documentation: Building with MPI Support," Qiskit Aer 0.17.1, 2025. [Online]. Available: https://qiskit.github.io/qiskit-aer/getting_started.html. Accessed: Aug. 9, 2026.

---

## Purpose

This documentation was reviewed to determine how Qiskit Aer can be used for distributed quantum-circuit simulation with MPI and how this capability could be incorporated into the QuantumHPC HPC execution framework.

---

## Summary

Qiskit Aer provides high-performance classical simulation of quantum circuits and supports MPI-based parallelization for cluster computing environments. MPI support allows Aer simulations to use multiple processes across a cluster, potentially increasing available memory and accelerating simulation through parallel computation.

Aer supports MPI both with and without GPU acceleration. The documentation identifies statevector, density matrix, and unitary simulation methods as methods that can be parallelized using MPI.

MPI support must be enabled when building Aer by configuring the build with the AER_MPI option. An MPI implementation such as Open MPI must also be installed and configured on the target system.

---

## Important Topics

- AerSimulator
- MPI-enabled Aer
- AER_MPI
- Distributed simulation
- Statevector simulation
- Density-matrix simulation
- Unitary simulation
- GPU + MPI
- Cluster execution
- Open MPI
- Parallel quantum simulation

---

## Relevance

- Distributed execution of Qiskit Aer
- Bridges-2 deployment
- MPI integration into QuantumHPC
- Future multi-node benchmarking
- GPU/MPI experimentation
- Determining the distinction between independent parallel experiments and distributed simulation of a single circuit

---

## Notes

- Qiskit Aer can use MPI to distribute simulation across cluster systems.
- MPI support can be used with or without GPU support.
- The documented MPI-supported simulation methods include statevector, density matrix, and unitary.
- MPI support is different from simply running several independent Python processes. Aer itself can use MPI to distribute a simulation.
- This creates two possible forms of parallelism for QuantumHPC:
  1. Distributing independent benchmark experiments across MPI processes.
  2. Using MPI-enabled Aer to distribute a single larger quantum simulation.
- The first approach appears to be the simpler initial implementation for QuantumHPC because the existing simulator can remain mostly independent of the MPI execution layer.
- The second approach may become important when testing larger quantum circuits or multi-node simulation.
- The Aer documentation therefore provides a direct connection between the current QuantumSimulator/Aer implementation and the planned MPI/HPC layer.