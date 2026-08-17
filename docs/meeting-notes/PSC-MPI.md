## Day 1 Personal Notes (8/3/26)
- *For reference, all mentions of "PE" is essentially talking about a core (PE = processing equipment). It can also refer to a processor*
- In Terminal/Command Line: ssh hartness@bridges2.psc.edu
- Communicator: MPI_Comm_rank (MPI_COMM,WORLD, &my_PE_num)
- Compiling (C and Fortran): mpicc hello.c
                             mpif90 hello.f
- MPI_Send( &numbertosend, 1, MPI_INT, 0, 10, MPI_COMM_WORLD)
- MPI_Recv( &numbertoreceive, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status)
- Receive/Message queue are important to understand. MPI_ANY_SOURCE and MPI_ANY_TAG can grab the next message in the queue.
- Messages from the same source will stay in order in the receive/message queue. Otherwise, order is not guaranteed.
- Mismatched data types are an error that may not be detected at runtime.
- When coding, you want to think serially, like you're starting as a single PE
- Manager and Worker PEs
- BARRIERs help restrict some code and allows output to be in order. Think about BARRIERs as brakes in a car. Do note, unnecessary BARRIERs may reduce performance, but properly used are essential.
- *AI for coding MPI isn't good about using BARRIERs, but BARRIERs are necessary for most scenarios.*
- Print statements for debugging:
    // Write the standard error (in C), which is unbuffered.
    fprintf(stderr, "PE %d\n", my_PE_num);
- MPI_Bcast() communicates some common data to every PE. Can replace using a for loop.
- Bcast and Reduce require all PE's to participate, all need to call the command at the same time
- MPI_Comm_size() gives basic information needed for the code to adjust itself.
- To enter an interactive environment: interact -n 8
- "Ghost cell" is a copy of the adjacent PE
- In C, memory in contiguous across rows. (elements need to be sent in a row [horizontal] direction)
- In Fortran, memory is contiguous across columns. (elemens need to be send in a column [vertical] direction)
- MPI_PROC_NULL is essentially a black hole / trash can for data

## Day 2 Personal Notes (8/4/26)
- Can code Halo codes in a 2D (vectors) or 3D configuration (3 types of messages, MPI_Type_create_subarray)
- Indexed block type is built to take indices from an array and use that for the message
- MPI_Type_free(&buffer_type) "frees up" indicated data type
- MPI_Get_count shows the count coming in
- Can restrict the amound of particles coming in by setting the max in MPI_Recv
- Can MPI_Probe the message, MPI_Get_count, MPI_Type_get_extent to get the number of particles needed for the message, malloc to dynamically allocate memory for the message, then MPI_Recv the determined amount of particles
- MPI_Aint is Address int and creates addresses of items in a linked list
- MPI_Get_address(item_to_send, &displacements[number_to_send]) will get the address of each item and put them into displacements array
- Can pack with MPI_Pack and MPI_Pack_size and unpack with MPI_Unpack
- Define and create structures (user-defined datatypes) with: MPI_Type_create_struct, MPI_Type_get_extent, and MPI_Type_create_resized
- Collective Communicators (all PE's need to participate): Bcast, Reduce, Scatter, Gather
- MPI_Scatter(void* send_data, int send_count, MPI_Datatype send_datatype, void* recv_data, int recv_count, MPI_Datatype recv_datatype, int root, MPI_Comm communicator) distributes different data/particles to multiple PE's from one PE
- MPI_Gather(void* send_data, int send_count, MPI_Datatype send_datatype, void* recv_data, int recv_count, MPI_Datatype recv_datatype, int root, MPI_Comm communicator) does the opposite of Scatterm filling one PE with different data from multiple PE's
- Multiple variations of Scatter and Gather: MPI_Scatterv(), MPI_Gatherv(), MPI_All...
- Can have sub Communicators with MPI_Comm_create(MPI_COMM_WORLD, group_worker, &comm_worker). Helpful for having a communicator separate from the primary/univsersal communication (e.g. MPI_COMM_WORLD). Basically, do this if you want to perform a collective communication task, but don't want all PE's to call it (want to exclude a PE from a collective task, like MPI_Reduce).
- Can also break an existing communicator into smaller pieces (communicators) with MPI_Comm_split(MPI_Comm comm, int color, int key, MPI_Comm *newcomm). "color" determines ordering withing the new communicator, and can just be treated like a variable.
- MPI_Comm_dup duplicates communicator(s)
- MPI has routines for Cartesian Topologies, namely: MPI_Cart_create(MPI_Comm comm_old, int ndims, const int dims[], int periods[], int reorder, MPI_Comm *comm_cart), MPI_Cart_shift(MPI_Comm comm, int direction, int disp, int *rank_source, int *rank_dest), MPI_Dims_create, MPI_cart_get, MPI_Cart_coords, and MPI_Cart_sub.
- MPI also allows for Graph Topologies (every neighbor only needs to know about its immediate neighbors)
- MPI_Neighbor_allgather is like a broadcast with all neighbors
- MPI_Neighbor_alltotal is like an exchange with all neighbors
- MPI has multiple commands and routines for creating and managing memory windows, which are basically regions of memory that can be worked with/on (MPI_Win...)
- MPI allows for hybrid programming (mixing with other models), such as OpenMP (omp.h) and GPU programming (CUDA)
- MPI has IO capabilities (MPI_IO)
- MPI has compatibility with at least C, Fortran 90, Python, Perl, R, Ruby, Java, and .NET
- *See PSC slides for Blocking, MPI_Sendrecv, Data Decomposition, Data Parallel, Threading, PGAS, and Frameworks*
- Python is a relatively simplistic and versatile language, but tends to be slow or poor performing
- C++ is becoming a significantly more popular language
- For Hybrid coding, if you do MPI first, then do the GPU later. MPI is very scalable and recommended to start with
- The future seems to be MPI+X, where X is some other program
- There are current two decent parallel debuggers: Totalview and DDT (both are proprietary, not open-source)