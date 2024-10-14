import os

home_dir = '/gpfs/projects/KimGroup/projects/nnUNet_milan'
slurm_files_dir = os.path.join(home_dir, 'slurm_files')
scripts_dir = os.path.join(home_dir, 'scripts')

tmplt_file = os.path.join(scripts_dir, '3.train_template.slurm')

if not os.path.exists(tmplt_file):
   print('template file not found:', tmplt_file) 
   exit(-1)

def schedule_train(dataset_num, configuration, fold, run, gen_predicted_probabilities):

    print(f'making slume file from template...{tmplt_file}')
    
    continue_train = run != 0

    with open(tmplt_file) as f:
        txt = f.read()

    # slurm case dir
    slurm_case_dir = os.path.join(slurm_files_dir, f"{dataset_num:03}")
    print(f'slurm_case_dir={slurm_case_dir}')
    if not os.path.exists(slurm_case_dir):
        os.makedirs(slurm_case_dir)

    # job_name, train_param
    job_name = f'train_{configuration}_fold{fold}_run{run}'
    train_params = f'{dataset_num} {configuration} {fold}'
    if continue_train:
        train_params = f'{train_params} --c'

    if gen_predicted_probabilities:
        train_params = f'{train_params} --npz'

    # save slurm file
    slurm_file = os.path.join(slurm_case_dir, f'train_{configuration}_fold{fold}_run{run}.slurm')

    #log file
    log_file = slurm_file + '.log'

    # replace variables
    txt = txt.replace('{job_name}', job_name)
    txt = txt.replace('{train_params}', train_params)
    txt = txt.replace('{log_file}', log_file)

    print(f'saving slurm_file - {slurm_file}')
    with open(slurm_file, 'w') as file:
        file.write(txt)

    # sbatch
    import subprocess
    
    cmd = f'module load slurm && sbatch {slurm_file}'
    print(f'running "{cmd}"')
    subprocess.run(cmd, shell=True)

def schedule_validation(dataset_num, configuration, fold, gen_predicted_probabilities):

    print(f'making slume file from template...{tmplt_file}')

    with open(tmplt_file) as f:
        txt = f.read()

    # slurm case dir
    slurm_case_dir = os.path.join(slurm_files_dir, f"{dataset_num:03}")
    print(f'slurm_case_dir={slurm_case_dir}')
    if not os.path.exists(slurm_case_dir):
        os.makedirs(slurm_case_dir)

    # job_name, train_param
    job_name = f'train_{configuration}_fold{fold}_val'
    train_params = f'{dataset_num} {configuration} {fold} --val'

    if gen_predicted_probabilities:
        train_params = f'{train_params} --npz'

    #log file
    log_file = os.path.join(slurm_case_dir, job_name+'.log')

    # replace variables
    txt = txt.replace('{job_name}', job_name)
    txt = txt.replace('{train_params}', train_params)
    txt = txt.replace('{log_file}', log_file)

    # save slurm file
    slurm_file = os.path.join(slurm_case_dir, f'train_{configuration}_fold{fold}_val.slurm')

    print(f'saving slurm_file - {slurm_file}')
    with open(slurm_file, 'w') as file:
        file.write(txt)

    # sbatch
    import subprocess
    
    cmd = f'module load slurm && sbatch {slurm_file}'
    print(f'running "{cmd}"')
    subprocess.run(cmd, shell=True)


#dataset_num = 9
dataset_num = 101
#dataset_num = 102
#dataset_num = 103

gen_predicted_probabilities = True # add --npz
#configuration='2d'
#configuration='3d_fullres'
#configuration='3d_lowres'
#configuration='3d_cascade_fullres'
validation_only = False

# basic unet - 4 runs were enough (for Dataset9_Spleen)
num_runs = 5

import time

if validation_only:
    for configuration in ['2d', '3d_fullres', '3d_lowres']:
        for fold in range(num_runs):
            print(f'=== fold: {fold} ===')
            schedule_validation(dataset_num, configuration, fold, gen_predicted_probabilities)
            time.sleep(3)
else:

    #for configuration in ['2d', '3d_fullres', '3d_lowres']:
    for configuration in ['3d_fullres']:
        for run in range(num_runs):
            for fold in range(5):
                print(f'=== fold: {fold} ===')
                schedule_train(dataset_num, configuration, fold, run, gen_predicted_probabilities)
                time.sleep(3)

# sbatch
print('done')