
import os
from config import get_config

config = get_config()

conf = '3d_lowres'
venv_dir = config['venv_dir']
scripts_dir = config['scripts_dir']
nnunet_dir = config['nnunet_dir']
data_dir = config['data_dir']

raw_dir = config['raw_dir']
preprocessed_dir= config['preprocessed_dir']
results_dir = config['results_dir']

slurm_files_dir = config['slurm_files_dir']

#dataset_name = 'Dataset009_Spleen'
#dataset_num = 9 #

#dataset_name = 'Dataset101_Eye[ul]L'
#dataset_num = 101

#dataset_name = 'Dataset102_ProneLumpStessin'
#dataset_num = 102

#dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART'
#dataset_num = 103

dataset_name = 'Dataset104_CBCTRectumBowel'
dataset_num = 104

dataset_results_dir = os.path.join(results_dir, dataset_name)

disable_ensembling = True

#configurations = '2d 3d_fullres 3d_lowres' 
configurations = conf
#configurations = '3d_fullres'

cmd_lines = f'nnUNetv2_find_best_configuration {dataset_num} -c {configurations} '
if disable_ensembling:
    cmd_lines = f'{cmd_lines} --disable_ensembling'

script_templete_file = os.path.join(scripts_dir, 'template.sh')
with open(script_templete_file, 'r') as file:
    txt = file.read()


txt = txt.replace('{venv_dir}', venv_dir)
txt = txt.replace('{data_dir}', data_dir)
txt = txt.replace('{nnunet_dir}', nnunet_dir)
txt = txt.replace('{cmd_lines}', cmd_lines)

configurations_encoded = configurations.replace('_','[us]')
script_file = os.path.join(dataset_results_dir, f'find_best_conf_{configurations_encoded}.sh')
with open(script_file, 'w') as file:
    file.write(txt)

# sbatch
import subprocess

cmd = f'chmod +x {script_file} && {script_file}'
print(f'running "{cmd}"')
subprocess.run(cmd, shell=True)

print('done')





