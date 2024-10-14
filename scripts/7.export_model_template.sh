cd /gpfs/projects/KimGroup/projects/nnUNet_milan
source ./_venv/bin/activate
cd src

export nnUNet_raw="/gpfs/projects/KimGroup/data/mic-mkfz/raw"
export nnUNet_preprocessed="/gpfs/projects/KimGroup/data/mic-mkfz/preprocessed"
export nnUNet_results="/gpfs/projects/KimGroup/data/mic-mkfz/results"

{cmd_lines}