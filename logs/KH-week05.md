# Week 05

**Date:** August 10 – August 16, 2026

---

# Goals

- Complete the planned QuantumHPC parameter sweep on Bridges-2.
- Evaluate the parameter-sweep results across the tested epsilon and simulation-noise conditions.
- Document the current HPC workflow and experimental progress.
- Update the project presentation with the Bridges-2 results.
- Create a project flowchart showing the completed work and the projected path for the remainder of the project.
- Prepare the project to transition from initial HPC setup into broader benchmarking and analysis.

---

# Approach & Implementation

Completed the connection between the QuantumHPC experiment framework and the Bridges-2 SLURM parameter-sweep workflow developed during Week 4. The parameter sweep was used to evaluate the planned combinations of the project's epsilon values and simulation conditions on the Bridges-2 compute environment.

The planned sweep consisted of four epsilon values, ε = {1, 2, 4, 8}, combined with three simulation conditions, for a total of 12 experimental conditions. The SLURM workflow was used to execute the experiments on Bridges-2 and collect the resulting runtime/output information.

Reviewed the completed parameter-sweep results and incorporated the relevant findings into the project's presentation and documentation. This provided the first completed HPC experiment set for the project and established a baseline for later performance comparisons.

Created and refined a project flowchart documenting the current QuantumHPC pipeline and the projected sequence of future work. The flowchart distinguishes completed work from upcoming tasks and provides a high-level view of the transition from the CPU/HPC baseline toward GPU experiments, MPI benchmarking, scaling studies, secondary-dataset experiments, and final project integration.

Maintained the project repository and documentation so that the completed Bridges-2 work and supporting materials remained synchronized with the current development state.
---

# Results

- Completed the planned Bridges-2 parameter-sweep evaluation.
- Evaluated the project's planned epsilon/noise-condition combinations through the HPC workflow.
- Established the first completed HPC experiment set for the QuantumHPC project.
- Incorporated Bridges-2 results into the project presentation and supporting documentation.
- Completed the project flowchart describing the current pipeline and projected future work.
- Established a clear transition point from initial HPC infrastructure development to performance benchmarking and analysis.
- Maintained a reproducible project structure through the GitHub repository and existing experiment/logging workflow.

---

# Next Steps

- Begin MPI-based parallelization of the quantum-simulation workload.
- Establish controlled MPI scaling experiments and collect runtime/speedup measurements.
- Begin GPU benchmarking on Bridges-2 and compare CPU and GPU execution.
- Begin the planned PhysioNet/NinaPro EMG secondary-dataset quantum-kernel extension.
- Coordinate with teammates on the interfaces needed to connect the HPC/MPI layer to the quantum-kernel and differential-privacy components.
- Begin transferring completed experimental results and methodology into the project Overleaf manuscript.
- Continue developing the HPC benchmarking workflow toward the project's later scaling and cross-resource experiments.

---

# References

- Qiskit Documentation
- Qiskit Aer Documentation
- MPI Forum Documentation
- LLNL MPI Tutorial
- Open MPI Documentation
- Bridges-2 User Documentation
- Project GitHub Repository
- Updated DREU-QIS 2026 Project Overview