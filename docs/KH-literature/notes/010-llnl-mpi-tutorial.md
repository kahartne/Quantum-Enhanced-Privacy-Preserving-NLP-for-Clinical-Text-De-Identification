# 010 – LLNL MPI Tutorial

## IEEE Reference

[10] B. Barney, "Message Passing Interface (MPI)," Lawrence Livermore National Laboratory, LLNL HPC Tutorials, UCRL-MI-133316. [Online]. Available: https://hpc-tutorials.llnl.gov/mpi/. Accessed: Aug. 9, 2026.

---

## Purpose

This tutorial provides an introduction to the Message Passing Interface (MPI) and distributed-memory parallel programming. It was used to develop foundational knowledge of MPI before integrating parallel execution into the QuantumHPC framework.

---

## Summary

The LLNL MPI tutorial introduces MPI as a standardized interface for communication between independent processes in distributed-memory systems. It covers the basic MPI programming model, environment management, point-to-point communication, collective communication, derived data types, and group/communicator management.

The tutorial explains the concept of MPI processes and ranks and demonstrates how processes can communicate using operations such as MPI_Send() and MPI_Recv(). It also introduces collective operations such as broadcast, scatter, gather, and reduction.

The tutorial includes examples in C, making it relevant to the planned C-based hardware integration work for QuantumHPC.

---

## Important Topics

- MPI_Init()
- MPI_Finalize()
- MPI_Comm_rank()
- MPI_Comm_size()
- MPI_COMM_WORLD
- MPI_Send()
- MPI_Recv()
- Blocking communication
- Non-blocking communication
- Collective communication
- Broadcast
- Scatter
- Gather
- Reduce
- Communicators
- Distributed-memory parallelism

---

## Relevance

- MPI architecture for QuantumHPC
- Distributed benchmark execution
- Multi-process execution
- Multi-node HPC execution
- Bridges-2 development
- Future C-based hardware integration
- Understanding rank and communicator concepts before implementing mpi_driver.py

---

## Notes

- MPI allows multiple independent processes to communicate and coordinate work.
- A rank identifies an individual MPI process within a communicator.
- MPI_COMM_WORLD is the default communicator containing the processes participating in the MPI program.
- MPI_Comm_size() determines the number of processes in the communicator.
- MPI_Comm_rank() determines the rank of the current process.
- Point-to-point communication allows one process to send information to another process.
- Collective operations allow processes within a communicator to participate in coordinated operations.
- MPI is particularly relevant to QuantumHPC because Bridges-2 uses distributed-memory compute nodes.
- The C examples in this tutorial are also relevant to the project's planned hardware-integration work.