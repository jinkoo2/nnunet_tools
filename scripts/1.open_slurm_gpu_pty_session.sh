module load slurm
srun -J test -N 1 -p a100-large --gres=gpu:4 --ntasks-per-node=28 --pty bash




