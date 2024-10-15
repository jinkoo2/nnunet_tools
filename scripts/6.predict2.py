
from dotenv import load_dotenv
import os

file = '/gpfs/projects/KimGroup/data/mic-mkfz/results/Dataset103_CBCT[sp]Bladders[sp]For[sp]ART/nnUNetTrainer__nnUNetPlans__2d/crossval_results_folds_0_1_2_3_4/postprocessing.pkl'


load_dotenv()

def _join_dir(dir1, dir2):
    joined = os.path.join(dir1, dir2)
    if not os.path.exists(joined):
        os.makedirs(joined)
    return joined

def _error(msg):
    raise Exception(f'Error: msg')

def _info(msg):
    print(msg)

def _must_exist(path):
    if not os.path.exists(path):
        raise Exception('Paht not found:{path}')
    
scripts_dir = os.getenv('scripts_dir')
nnunet_dir = os.getenv('nnunet_dir')
data_dir = os.getenv('data_dir')

if not os.path.exists(scripts_dir):
    _error(f'scripts_dir not found:{scripts_dir}')

if not os.path.exists(nnunet_dir):
    _error(f'nnunet_dir not found:{nnunet_dir}')

if not os.path.exists(data_dir):
    _error(f'data_dir not found:{data_dir}')

raw_dir = _join_dir(data_dir, 'raw')
preprocessed_dir= _join_dir(data_dir, 'preprocessed')
results_dir = _join_dir(data_dir, 'results')

slurm_files_dir = _join_dir(data_dir, 'slurm_files')


#dataset_name = 'Dataset009_Spleen'
#dataset_num = 9

#dataset_name = 'Dataset101_Eye[ul]L'
#dataset_num = 101

#dataset_name = 'Dataset102_ProneLumpStessin'
#dataset_num = 102

dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART'
dataset_num = 103

use_slurm = False

dataset_results_dir = _join_dir(results_dir, dataset_name)

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


def schedule_predict(dataset_num, cmd_lines):

    tmplt_file = os.path.join(scripts_dir, '6.predict_template.slurm')

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
    txt = txt.replace('{scripts_dir}', scripts_dir)
    txt = txt.replace('{nnunet_dir}', nnunet_dir)
    txt = txt.replace('{data_dir}', data_dir)

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
        file.write(f'cd {nnunet_dir}\n')

        # export
        file.write(f'export nnUNet_raw="{raw_dir}"\n')
        file.write(f'export nnUNet_preprocessed="{preprocessed_dir}"\n')
        file.write(f'export nnUNet_results="{results_dir}"\n')
        
        # predition
        pred_i = f'{raw_dir}/{dataset_name}/imagesTs'
        pred_o = f'{pred_i}/predict'
        pred_f = '0 1 2 3 4'
        pred_tr = 'nnUNetTrainer'
        pred_c = '2d'
        pred_p = 'nnUNetPlans'
        pred_d = 'cpu'
        pred_cmd = f'nnUNetv2_predict -d {dataset_name} -i {pred_i} -o {pred_o} -f  {pred_f} -tr {pred_tr}  -c {pred_c} -p {pred_p} -device {pred_d}\n'
        _info(pred_cmd)
        file.write(pred_cmd)

        _must_exist(pred_i)

        # post processing
        pp_i =  pred_o  
        pp_o = _join_dir(pred_o, 'pp')
        folds_str = pred_f.replace(' ', '_')
        cross_val_results_dir = f'{dataset_results_dir}/{pred_tr}__{pred_p}__{pred_c}/crossval_results_folds_{folds_str}'
        pp_pkl_file=f'{cross_val_results_dir}/postprocessing.pkl'
        pp_np=8
        pp_plans_json=f'{cross_val_results_dir}/plans.json'
        pp_cmd = f'nnUNetv2_apply_postprocessing -i {pp_i} -o {pp_o} -pp_pkl_file {pp_pkl_file} -np {pp_np} -plans_json {pp_plans_json}\n'
        _info(pp_cmd)
        file.write(pp_cmd)

        _must_exist(pp_i)
        _must_exist(cross_val_results_dir)
        _must_exist(pp_pkl_file)
        _must_exist(pp_plans_json)

    # sbatch
    import subprocess

    cmd = f'chmod +x {script_file} && {script_file}'
    print(f'running "{cmd}"')
    subprocess.run(cmd, shell=True)

print('done')






