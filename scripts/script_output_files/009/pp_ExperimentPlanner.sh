cd /gpfs/projects/KimGroup/projects/nnUNet_milan/_venv
source ./bin/activate
cd /gpfs/projects/KimGroup/projects/nnUNet_milan/src

export nnUNet_raw="/gpfs/projects/KimGroup/data/mic-mkfz/raw"
export nnUNet_preprocessed="/gpfs/projects/KimGroup/data/mic-mkfz/preprocessed"
export nnUNet_results="/gpfs/projects/KimGroup/data/mic-mkfz/results"

nnUNetv2_plan_and_preprocess -d 9 -pl ExperimentPlanner --verbose 2>&1 | tee /gpfs/projects/KimGroup/projects/nnUNet_milan/scripts/script_output_files/009/pp_ExperimentPlanner.sh.log 