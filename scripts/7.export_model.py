
import os

home_dir = '/gpfs/projects/KimGroup/projects/nnUNet_milan'
slurm_files_dir = os.path.join(home_dir, 'slurm_files')
scripts_dir = os.path.join(home_dir, 'scripts')
src_dir = os.path.join(home_dir, 'src')

data_dir = '/gpfs/projects/KimGroup/data/mic-mkfz'
raw_dir = os.path.join(data_dir, 'raw')
results_dir = os.path.join(data_dir, 'results')

dataset_name = 'Dataset009_Spleen'
dataset_num = 9 #

#dataset_name = 'Dataset101_Eye[ul]L'
#dataset_num = 101

#dataset_name = 'Dataset102_ProneLumpStessin'
#dataset_num = 102

dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART'
dataset_num = 103

dataset_results_dir = os.path.join(results_dir, dataset_name)

configurations = '2d 3d_fullres 3d_lowres'
zip_file = os.path.join(dataset_results_dir, 'model.zip' )
cmd_lines = f'nnUNetv2_export_model_to_zip -d {dataset_num} -o {zip_file} -c {configurations} --exp_cv_preds'

script_templete_file = os.path.join(scripts_dir, '7.export_model_template.sh')
with open(script_templete_file, 'r') as file:
    txt = file.read()

txt = txt.replace('{cmd_lines}', cmd_lines)

script_file = os.path.join(dataset_results_dir, 'export_model.sh')
with open(script_file, 'w') as file:
    file.write(txt)

# sbatch
import subprocess

cmd = f'chmod +x {script_file} && {script_file}'
print(f'running "{cmd}"')
subprocess.run(cmd, shell=True)

print('done')





