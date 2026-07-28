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

Reviewed Qiskit's documentation and several introductory resources to build familiarity with the syntax and core concepts before getting into the code. Installed Qiskit and Qiskit Aer and tested the setup with a simple 2 qubit circuit before moving into the required circuits. Built the Bell state and GHZ state circuits using only Hadamard and CNOT gates, and separately tested the X, H, and Z gates on their own to confirm my understanding of each gate before combining them. For the ZZFeatureMap, I constructed it manually with a layer of Hadamards, a layer encoding each input feature with an RZ rotation, and a CX RZ CX block to encode the interaction between features, first at 2 qubits, then extended to 4. For every circuit, I also pulled the statevector directly, in addition to measurement counts, to confirm the actual quantum state matched expectations. Attended the Week 1-2 check-in meeting with Dr. Mahajan, Edmund, and Kyle to review progress and align on next steps.

---

# Results

- Bell and GHZ states came out entangled as expected. Measurements landed only on the all 0 or all 1 outcomes, never a mix.
- ZZFeatureMap worked correctly at both 2 and 4 qubits and the resulting state changed depending on the input feature values.
- All three circuits are documented in notebooks and pushed to my branch on the team repo.

---

# Next Steps

- Load the i2b2/MIMIC III placeholder dataset and count PHI category frequencies.
- Start a literature review spreadsheet covering NLP techniques, quantum techniques, and privacy preserving techniques.
- Start on the baseline system and SHAP implementation.

---

# References

- Qiskit Documentation
- Qiskit Aer Documentation
