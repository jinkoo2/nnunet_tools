module load slurm
srun -J test -N 1 -p gpu-large --ntasks-per-node=28 --pty bash


