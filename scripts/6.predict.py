
import os

home_dir = '/gpfs/projects/KimGroup/projects/nnUNet_milan'
slurm_files_dir = os.path.join(home_dir, 'slurm_files')
scripts_dir = os.path.join(home_dir, 'scripts')
src_dir = os.path.join(home_dir, 'src')

data_dir = '/gpfs/projects/KimGroup/data/mic-mkfz'
raw_dir = os.path.join(data_dir, 'raw')
results_dir = os.path.join(data_dir, 'results')

#dataset_name = 'Dataset009_Spleen'
#dataset_num = 9

#dataset_name = 'Dataset101_Eye[ul]L'
#dataset_num = 101

#dataset_name = 'Dataset102_ProneLumpStessin'
#dataset_num = 102

dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART'
dataset_num = 103

use_slurm = True

dataset_results_dir = os.path.join(results_dir, dataset_name)

inference_instruction_file = os.path.join(dataset_results_dir, 'inference_instructions.txt')
script_tmpl_file = os.path.join(dataset_results_dir, 'predict.templ.sh')
def make_predict_shell_script(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            stripped_line = line.strip()
            if stripped_line.startswith("nnUNetv2"):
                outfile.write(line)

make_predict_shell_script(inference_instruction_file, script_tmpl_file)

imagesTs_dir = os.path.join(os.path.join(raw_dir, dataset_name), 'imagesTs')
labelsTs_model1 = os.path.join(os.path.join(raw_dir, dataset_name), '1.labels_model1')
labelsTs_model2 = os.path.join(os.path.join(raw_dir, dataset_name), '2.labels_model2')
labelsTs_predict = os.path.join(os.path.join(raw_dir, dataset_name), '3.labels_predict')
labelsTs_predict_pp = os.path.join(os.path.join(raw_dir, dataset_name), '4.labels_predict_pp')

INPUT_FOLDER = imagesTs_dir
OUTPUT_FOLDER_MODEL1 = labelsTs_model1
OUTPUT_FOLDER_MODEL2 = labelsTs_model2
OUTPUT_FOLDER = labelsTs_predict
OUTPUT_FOLDER_PP = labelsTs_predict_pp

with open(script_tmpl_file, 'r') as f:
     cmd_lines = f.read()

cmd_lines = cmd_lines.replace('INPUT_FOLDER', INPUT_FOLDER)
cmd_lines = cmd_lines.replace('OUTPUT_FOLDER_MODEL_1', OUTPUT_FOLDER_MODEL1)
cmd_lines = cmd_lines.replace('OUTPUT_FOLDER_MODEL_2', OUTPUT_FOLDER_MODEL2)
cmd_lines = cmd_lines.replace('OUTPUT_FOLDER_PP', OUTPUT_FOLDER_PP)
cmd_lines = cmd_lines.replace('OUTPUT_FOLDER', OUTPUT_FOLDER)

tmplt_file = os.path.join(scripts_dir, '6.predict_template.slurm')
def schedule_predict(dataset_num, cmd_lines):

    print(f'making slume file from template...{tmplt_file}')
    
    with open(tmplt_file) as f:
        txt = f.read()

    # slurm case dir
    slurm_case_dir = os.path.join(slurm_files_dir, f"{dataset_num:03}")
    print(f'slurm_case_dir={slurm_case_dir}')
    if not os.path.exists(slurm_case_dir):
        os.makedirs(slurm_case_dir)

    # job_name, train_param
    job_name = f'predict_{dataset_num}'

    # save slurm file
    slurm_file = os.path.join(slurm_case_dir, f'predict.slurm')

    #log file
    log_file = slurm_file + '.log'

    # replace variables
    txt = txt.replace('{job_name}', job_name)
    txt = txt.replace('{log_file}', log_file)
    txt = txt.replace('{cmd_lines}', cmd_lines)

    print(f'saving slurm_file - {slurm_file}')
    with open(slurm_file, 'w') as file:
        file.write(txt)

    # sbatch
    import subprocess
    
    cmd = f'module load slurm && sbatch {slurm_file}'
    print(f'running "{cmd}"')
    subprocess.run(cmd, shell=True)

if use_slurm:
    schedule_predict(dataset_num, cmd_lines)
else: # run as a shell script
    script_file = os.path.join(dataset_results_dir, 'predict.sh')
    with open(script_file, 'w') as file:
        
        #switch to the base
        file.write(f'cd {src_dir}\n')

        # export
        file.write('export nnUNet_raw="/gpfs/projects/KimGroup/data/mic-mkfz/raw"\n')
        file.write('export nnUNet_preprocessed="/gpfs/projects/KimGroup/data/mic-mkfz/preprocessed"\n')
        file.write('export nnUNet_results="/gpfs/projects/KimGroup/data/mic-mkfz/results"\n')
        
        file.write(cmd_lines)

    # sbatch
    import subprocess

    cmd = f'chmod +x {script_file} && {script_file}'
    print(f'running "{cmd}"')
    subprocess.run(cmd, shell=True)

print('done')






