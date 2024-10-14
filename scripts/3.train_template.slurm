#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={log_file}
#SBATCH --ntasks-per-node=28
#SBATCH --nodes=1
#SBATCH --time=03:00:00
#SBATCH -p a100-large
#SBATCH --gres=gpu:4            # number of GPUs per node (gres=gpu:N)
#SBATCH --gpus=4 # number of GPUs per node (gres=gpu:N), this is a backup of --gres
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jinkoo.kim@stonybrook.edu

cd /gpfs/projects/KimGroup/projects/nnUNet_milan
source ./_venv/bin/activate
cd src

export nnUNet_raw="/gpfs/projects/KimGroup/data/mic-mkfz/raw"
export nnUNet_preprocessed="/gpfs/projects/KimGroup/data/mic-mkfz/preprocessed"
export nnUNet_results="/gpfs/projects/KimGroup/data/mic-mkfz/results"

nnUNetv2_train {train_params} 
