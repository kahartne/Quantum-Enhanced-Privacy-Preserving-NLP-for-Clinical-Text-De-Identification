# 013 – Pittsburgh Supercomputing Center MPI Programming Workshop

## Reference

[13] J. Urbanic, "Pittsburgh Supercomputing Center MPI Programming Workshop," Pittsburgh Supercomputing Center, Aug. 3–4, 2026.

---

## Purpose

The Pittsburgh Supercomputing Center MPI Programming Workshop was used to develop practical knowledge of MPI programming, distributed-memory parallelism, domain decomposition, scalable programming, and HPC execution on Bridges-2.

The workshop material was reviewed with emphasis on C programming and MPI. Fortran examples were not used in the QuantumHPC implementation.

---

## Topics Covered

- HPC computing environment
- Parallel computing concepts
- Strong and weak scaling
- Amdahl's Law
- Message-passing programming
- MPI processes and ranks
- Domain decomposition
- Point-to-point communication
- Blocking communication
- Deadlocks
- Ghost-zone communication
- Non-blocking communication
- Persistent communication
- MPI_Sendrecv
- MPI_Isend / MPI_Irecv
- MPI_Waitall
- MPI_Send_init / MPI_Recv_init
- MPI + OpenMP hybrid programming
- Parallel debugging
- Parallel profiling
- Bridges-2 execution

---

## Key Lessons

### Domain Decomposition

A major principle of MPI programming is identifying the primary data structures and dividing those structures among processing elements. Changes to the decomposition generally require changes to code associated with boundaries, communication, and I/O, while the underlying computational kernel may remain largely unchanged.

### Communication

Blocking MPI communication can produce deadlocks when processes wait on one another. Communication order and synchronization must therefore be considered carefully.

Non-blocking communication can avoid some synchronization problems and allow communication to overlap with useful computation.

### Scalability

Parallel performance should be evaluated through strong and weak scaling. Increasing the number of processors does not automatically produce proportional speedup because serial work, communication, and synchronization can become limiting factors.

### MPI vs. OpenMP

OpenMP is primarily constrained to resources within a single node, while MPI can distribute work across multiple networked nodes. MPI and OpenMP can also be combined in hybrid programs.

---

## Relevance to QuantumHPC

The workshop provides the practical HPC foundation for the planned QuantumHPC MPI implementation.

The existing QuantumHPC simulator performs quantum-circuit simulation using Qiskit Aer. MPI can potentially be introduced as a parallel execution layer around the simulator, allowing independent simulations or benchmark conditions to be distributed across processes and eventually across Bridges-2 nodes.

The workshop's discussion of domain decomposition provides a framework for determining what portion of the QuantumHPC workload should be distributed.

The discussion of scalability is also directly relevant to evaluating the QuantumHPC implementation through processor-count, runtime, speedup, and efficiency measurements.

---

## Notes

- MPI should be viewed as a distributed-memory programming model rather than simply a method for launching multiple copies of a program.
- Rank identifies an MPI process within a communicator.
- Work and data must be intentionally divided among processes.
- Communication patterns must be designed to avoid deadlocks and unnecessary serialization.
- A program that works with a small number of processes may still fail or scale poorly at larger process counts.
- Strong and weak scaling should be considered when evaluating the eventual QuantumHPC MPI implementation.
- MPI is appropriate for QuantumHPC because the project ultimately targets multi-node execution on Bridges-2.
- C will be used for MPI learning and implementation where possible.
- The Laplace exercise is useful as a model for thinking about domain decomposition, even though the initial QuantumHPC workload may be more naturally divided by independent simulation tasks rather than grid regions.