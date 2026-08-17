# Week 01

**Date:** July 25 – July 31, 2026

---

# Goals

- Finalize the project repository and documentation workflow.
- Continue building a literature/reference trail that supports the project implementation.
- Investigate MPI and determine how it may fit into the QuantumHPC simulation framework.
- Begin comparing available HPC platforms and identify the requirements for future benchmarking.

---

# Approach & Implementation

Continued organizing the team's GitHub repository and project documentation, including the literature review, references, README, and repository-management materials. Expanded the literature review beyond Qiskit/Aer documentation to include MPI and HPC resources.

Investigated MPI as a possible parallelization layer for the quantum simulation work. Reviewed MPI fundamentals including ranks, communicators, point-to-point communication, collective operations, and distributed-memory execution. Also began considering how MPI could fit alongside Qiskit Aer rather than replacing the existing simulation framework.

Began investigating the available computing platforms, particularly Bridges-2 and Jetstream2, with the goal of determining which environment is most appropriate for the project's eventual benchmarking and distributed simulation work. C was identified as a useful language for the hardware/integration portion of the project based on the HPC direction and the planned MPI work.
---

# Results

- Continued establishing a structured GitHub repository for the team.
- Expanded the project's literature/documentation collection to include MPI and HPC resources.
- Identified MPI as a relevant technology for distributing future quantum-simulation workloads.
- Began connecting the existing Qiskit/Aer work to a larger HPC execution environment.
- Identified Bridges-2 as a practical target for MPI experimentation and future scaling tests.
- Prepared for the PSC MPI workshop and the transition from local development toward HPC-based testing.
---

# Next Steps

- Attend and complete the PSC MPI workshop.
- Implement and test a basic C MPI program.
- Set up and test the QuantumHPC repository on Bridges-2.
- Develop a preliminary SLURM parameter-sweep workflow.
- Continue refining the relationship between the Qiskit/Aer simulation layer and the HPC execution layer.
- Begin planning actual benchmark experiments once the execution environment is established.
---

# References

- Qiskit Documentation
- Qiskit Aer Documentation
- Git Documentation
- GitHub Documentation
- MPI Forum Documentation
- LLNL MPI Tutorial
- Open MPI Documentation
- Bridges-2 User Documentation