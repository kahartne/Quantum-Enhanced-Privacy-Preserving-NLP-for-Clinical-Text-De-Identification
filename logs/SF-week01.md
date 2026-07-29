# Week 1

**Date:** July 13 – July 20, 2026

---

# Goals

- Learn the fundamentals of quantum computing and Qiskit.
- Set up my environment and confirm everything runs correctly.
- Build Bell states, GHZ states, and individual single-qubit gates.
- Implement the ZZFeatureMap gate by gate, without using Qiskit's built-in feature map class.

---

# Approach & Implementation

Reviewed Qiskit's documentation and several introductory resources to build familiarity with the syntax and core concepts before getting into the code. Installed Qiskit and Qiskit Aer and tested the setup with a simple 2 qubit circuit before moving into the required circuits. Built the Bell state and GHZ state circuits using only Hadamard and CNOT gates, and separately tested the X, H, and Z gates on their own to confirm my understanding of each gate before combining them. Constructed the ZZFeatureMap manually using Hadamard, RZ, and CX gates to encode input features and their interactions, first at 2 qubits then extended to 4. For each circuit, I examined the measurement counts and statevector to confirm the circuit behaved as expected. 

---

# Results

- Bell and GHZ states came out entangled as expected. Measurements landed only on the all 0 or all 1 outcomes, never a mix.
- ZZFeatureMap worked correctly at both 2 and 4 qubits and the resulting state changed depending on the input feature values.
- All three circuits are documented in notebooks and pushed to my branch on the team repo.

---

# Next Steps

- Prepare project presentation.
- Load the i2b2/MIMIC III placeholder dataset and count PHI categories.
- Start a literature review spreadsheet on NLP, quantum, and privacy preserving techniques.

---

# References

- Qiskit Documentation
- Qiskit Aer Documentation
