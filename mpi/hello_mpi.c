#include <stdio.h>
#include <mpi.h>

// MPI enviornment will be provided by the target HPC system.

int main(int argc, char *argv[])
{
    int rank, size;

    MPI_Init(&argc, &argv); // Starts MPI

    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // Determines current process
    MPI_Comm_size(MPI_COMM_WORLD, &size); // Determines number of processes

    printf("Hello from rank %d of %d\n", rank, size);

    MPI_Finalize(); // Shuts down MPI

    return 0;
}