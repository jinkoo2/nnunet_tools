#!/bin/bash
#SBATCH --job-name=pp_ds9
#SBATCH --output=/gpfs/projects/KimGroup/projects/nnUNet_milan/scripts/script_output_files/009/pp_ExperimentPlanner.slurm.log
#SBATCH --ntasks-per-node=28
#SBATCH --nodes=1
#SBATCH --time=08:00:00
#SBATCH -p a100-large
#SBATCH --gres=gpu:1            # number of GPUs per node (gres=gpu:N)
#SBATCH --gpus=1 # number of GPUs per node (gres=gpu:N), this is a backup of --gres
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jinkoo.kim@stonybrook.edu

cd /gpfs/projects/KimGroup/projects/nnUNet_milan/_venv
source ./bin/activate
cd /gpfs/projects/KimGroup/projects/nnUNet_milan/src

export nnUNet_raw="/gpfs/projects/KimGroup/data/mic-mkfz/raw"
export nnUNet_preprocessed="/gpfs/projects/KimGroup/data/mic-mkfz/preprocessed"
export nnUNet_results="/gpfs/projects/KimGroup/data/mic-mkfz/results"

nnUNetv2_plan_and_preprocess -d 105 -pl ExperimentPlanner --verbose --verify_dataset_integrity  