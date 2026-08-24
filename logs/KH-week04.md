# Week 04

**Date:** August 3 – August 9, 2026

---

# Goals

- Learn practical MPI programming and HPC workflow through the PSC workshop.
- Establish a working MPI environment on Bridges-2.
- Begin implementing the HPC execution infrastructure for the QuantumHPC project.
- Develop a preliminary SLURM parameter-sweep workflow.

---

# Approach & Implementation

Attended the Pittsburgh Supercomputing Center MPI/HPC workshop and worked through the C-based MPI exercises. Focused on MPI initialization, ranks, communicators, point-to-point communication, collective communication, synchronization, data decomposition, and the general manager/worker model. The workshop also introduced more advanced concepts including ghost cells, derived datatypes, communicator management, Cartesian topologies, and hybrid MPI programming. Personal workshop notes and C exercises were preserved for later reference.

Set up access to Bridges-2 and verified the available MPI environment. Used the Bridges-2 login environment to inspect available Open MPI modules and identify the MPI compiler wrapper. The workshop materials describe compiling C programs with mpicc and running MPI executables with mpirun, which was subsequently applied to the QuantumHPC project.

Created a basic hello_mpi.c program in the project's mpi/ directory and compiled it with mpicc. Successfully executed the program with four MPI processes on a Bridges-2 compute node, confirming that the repository can be built and executed in the target HPC environment.

Created slurm/parameter_sweep.slurm as a preliminary job-array skeleton for the project's planned parameter sweep. The script represents the 12 planned combinations of ε = {1, 2, 4, 8} and three simulation conditions. A single array task was submitted and successfully executed on a Bridges-2 regular-memory compute node. The task correctly mapped array index 0 to ε = 1 and the noiseless condition and wrote its output to results/logs/.

Also began investigating the Jetson Nano as an additional project hardware target. This reinforced the need for the project software architecture to remain portable across local, HPC, GPU, and embedded environments.
---

# Results

- Completed the PSC MPI workshop and recovered the workshop notes and C exercises for continued reference.
- Established a working MPI development environment on Bridges-2.
- Successfully compiled the project's C MPI test program using mpicc.
- Successfully executed four MPI ranks on a Bridges-2 compute node.
- Created and tested the initial SLURM parameter-sweep infrastructure.
- Successfully executed one SLURM array task on a Bridges-2 compute node.
- Verified that the SLURM task correctly assigned an experiment parameter combination and generated an output log.
- Established a concrete connection between the existing QuantumHPC simulation framework and the target HPC execution environment.

---

# Next Steps

- Connect the SLURM parameter sweep to the actual QuantumHPC simulation entry point.
- Determine how MPI should distribute quantum-kernel/simulation workloads.
- Compare single-process, MPI, and GPU execution once the experiment interface is ready.
- Continue evaluating Bridges-2 and other available compute resources for the project's benchmarking requirements.
- Begin testing the framework with a real dataset when the simulation and experiment-management layers are ready.
- Incorporate the recovered workshop material and relevant HPC research into the project's literature review and research manuscript.

---

# References

- PSC MPI Workshop Materials
- LLNL MPI Tutorial
- Open MPI Documentation
- MPI Forum Documentation
- Qiskit Aer MPI Documentation
- Bridges-2 User Documentation
- Brown et al., “Multi-GPU Quantum Circuit Simulation, Enabled by MPI, Benchmarks HPC System Performance”