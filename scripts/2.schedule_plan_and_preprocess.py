import os

home_dir = '/gpfs/projects/KimGroup/projects/nnUNet_milan'
slurm_files_dir = os.path.join(home_dir, 'slurm_files')
scripts_dir = os.path.join(home_dir, 'scripts')

tmplt_file = __file__.replace('.py', '.slurm') 

if not os.path.exists(tmplt_file):
   print('template file not found:', tmplt_file) 
   exit(-1)

def schedule_plan_and_preprocess(dataset_num, planner, verify_dataset_integrity):

    print(f'making slume file from template...{tmplt_file}')

    with open(tmplt_file) as f:
        txt = f.read()

    # slurm case dir
    slurm_case_dir = os.path.join(slurm_files_dir, f"{dataset_num:03}")
    print(f'slurm_case_dir={slurm_case_dir}')
    if not os.path.exists(slurm_case_dir):
        os.makedirs(slurm_case_dir)

    # job_name, train_param
    job_name = f'pp_{planner}_ds{dataset_num}'
    cmd_args = f'-d {dataset_num} -pl {planner}'

    if verify_dataset_integrity:
        cmd_args = f'{cmd_args} --verify_dataset_integrity'

    # save slurm file
    slurm_file = os.path.join(slurm_case_dir, f'pp_{planner}.slurm')

    #log file
    log_file = slurm_file+'.log'

    # replace variables
    txt = txt.replace('{job_name}', job_name)
    txt = txt.replace('{cmd_args}', cmd_args)
    txt = txt.replace('{log_file}', log_file)



    print(f'saving slurm_file - {slurm_file}')
    with open(slurm_file, 'w') as file:
        file.write(txt)

    # sbatch
    import subprocess
    
    cmd = f'module load slurm && sbatch {slurm_file}'
    print(f'running "{cmd}"')
    subprocess.run(cmd, shell=True)


#dataset_num = 9 # Dataset009_Spleen
#dataset_num = 101 # Dataset101_Eye[ul]L
#dataset_num = 102 # Dataset102_ProneLumpStessin
dataset_num = 103

verify_dataset_integrity = True
planner='ExperimentPlanner'
#planner='nnUNetPlannerResEncM'
#planner='nnUNetPlannerResEncL'
#planner='nnUNetPlannerResEncXL'

schedule_plan_and_preprocess(dataset_num, planner, verify_dataset_integrity)

# sbatch
print('done')



