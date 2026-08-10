# 012 – Bridges-2 User Guide and SLURM Batch Execution

## IEEE Reference

[12] Pittsburgh Supercomputing Center, "Bridges-2 User Guide," Carnegie Mellon University. [Online]. Available: https://www.psc.edu/resources/bridges-2/user-guide/. Accessed: Aug. 9, 2026.

---

## Purpose

The Bridges-2 User Guide was reviewed to understand how QuantumHPC will be executed on the target HPC system, particularly the use of SLURM for allocating compute resources and submitting batch jobs.

---

## Summary

Bridges-2 uses the SLURM workload manager to allocate compute resources and manage jobs. Production computing is performed on compute nodes rather than login nodes.

Bridges-2 supports interactive sessions, batch jobs, and OnDemand execution. Batch execution uses a job script containing resource requests and commands, which is submitted to SLURM using the sbatch command.

SLURM options can specify the partition, walltime, number of nodes, number of tasks or cores, output files, GPU resources, and allocation ID. Bridges-2 also supports job arrays for submitting collections of similar jobs.

---

## Important Topics

- SLURM
- sbatch
- srun
- Interactive jobs
- Batch jobs
- Compute nodes
- Login nodes
- Partitions
- Walltime
- Nodes
- Tasks
- GPU allocation
- Allocation IDs
- Job arrays
- Job output
- Bridges-2 GPU resources

---

## Relevance

- Bridges-2 deployment
- HPC execution environment
- MPI job execution
- QuantumHPC benchmark sweeps
- GPU resource allocation
- Reproducible batch execution
- Future parameter sweeps
- SLURM batch-script development

---

## Notes

- Production computation should be performed on Bridges-2 compute nodes rather than login nodes.
- SLURM manages the allocation of compute resources.
- A batch job is defined by a script and submitted using sbatch.
- The batch script can specify resources such as nodes, tasks, walltime, partition, and GPUs.
- srun can be used to launch commands within an allocated job.
- The correct SLURM allocation ID must be used when required.
- Bridges-2 provides different partitions depending on the resources included in the user's allocation.
- GPU partitions can provide multiple GPUs and multiple nodes, making them relevant to future QuantumHPC GPU/MPI experiments.
- SLURM job arrays may eventually be useful for running collections of similar benchmark conditions.
- The initial QuantumHPC SLURM script should remain simple until the correct account, partition, resource requirements, and software environment are confirmed on Bridges-2.