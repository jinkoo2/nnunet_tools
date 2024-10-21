cd {venv_dir}
source ./bin/activate
cd {nnunet_dir}

export nnUNet_raw="{data_dir}/raw"
export nnUNet_preprocessed="{data_dir}/preprocessed"
export nnUNet_results="{data_dir}/results"

{cmd_lines}