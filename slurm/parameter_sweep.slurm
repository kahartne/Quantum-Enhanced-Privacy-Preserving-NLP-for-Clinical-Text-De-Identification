#!/bin/bash

#SBATCH --job-name=quantumhpc-sweep       # Job name
#SBATCH --nodes=1                         # Request 1 computing node
#SBATCH --ntasks=4                        # Request 4 MPI tasks/processes
#SBATCH --time=00:10:00                   # Maximum requested runtime
#SBATCH --array=0-11                      # 12 array tasks for 12 experiments (4 epsilon values x 3 conditions)
#SBATCH --output=results/slurm-%A_%a.out  # Save output to file (%j becomes job ID)

# Load the appropriate compiler/MPI environment.
# The exact module names to be determined on Bridges-2.

# Each array task represents one parameter combination
echo "QuantumHPC parameter sweep"
echo "Job ID: $SLURM_ARRAY_JOB_ID"
echo "Task ID: $SLURM_ARRAY_TASK_ID"

# Future:
# python main.py --experiment $SLURM_ARRAY_TASK_ID