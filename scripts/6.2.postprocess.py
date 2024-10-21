
import os
from utils import _error, _info, _join_dir, _must_exist, get_current_datetime_str, copy_file_to_folder
import utils
from config import get_config


def postprocess(
        dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART', 
        dataset_num = 103,
        round = 'r2',
        conf = '3d_lowres',
        folds = '0 1 2 3 4',
        plan = 'nnUNetPlans',
        trainer = 'nnUNetTrainer',
        use_slurm = False,
        )->None:

    config = get_config()
        
    scripts_dir = config['scripts_dir']
    nnunet_dir = config['nnunet_dir']
    data_dir = config['data_dir']

    raw_dir = config['raw_dir']
    preprocessed_dir= config['preprocessed_dir']
    results_dir = config['results_dir']

    

    conf_encoded = conf.replace('_', '[us]')

    dataset_results_dir = _join_dir(results_dir, dataset_name)

    #imagesTs_dir = os.path.join(os.path.join(raw_dir, dataset_name), f'{round}_imagesTs')
    labelsTs_predict = os.path.join(os.path.join(raw_dir, dataset_name), f'{round}_{conf_encoded}_predict')
    labelsTs_predict_pp = os.path.join(labelsTs_predict, 'pp')

    # post processing
    pp_i =  labelsTs_predict  
    pp_o = labelsTs_predict_pp
    folds_str = folds.replace(' ', '_')
    cross_val_results_dir = f'{dataset_results_dir}/{trainer}__{plan}__{conf}/crossval_results_folds_{folds_str}'
    pp_pkl_file=f'{cross_val_results_dir}/postprocessing.pkl'
    pp_np=8
    pp_plans_json=f'{cross_val_results_dir}/plans.json'
    pp_cmd = f'nnUNetv2_apply_postprocessing -i {pp_i} -o {pp_o} -pp_pkl_file {pp_pkl_file} -np {pp_np} -plans_json {pp_plans_json}\n'
    _info(pp_cmd)

    _must_exist(pp_i)
    _must_exist(cross_val_results_dir)
    _must_exist(pp_pkl_file)
    _must_exist(pp_plans_json)

    cmd_lines = f'{pp_cmd}\n'

    if use_slurm:

        slurm_files_dir = config['slurm_files_dir']

        tmplt_file = os.path.join(scripts_dir, 'template.slurm')

        print(f'making slume file from template...{tmplt_file}')
        
        with open(tmplt_file) as f:
            txt = f.read()

        # slurm case dir
        slurm_case_dir = os.path.join(slurm_files_dir, f"{dataset_num:03}")
        print(f'slurm_case_dir={slurm_case_dir}')
        if not os.path.exists(slurm_case_dir):
            os.makedirs(slurm_case_dir)

        # job_name, train_param
        job_name = f'predict_{dataset_num}_{round}_{conf_encoded}'

        # slurm file
        slurm_file = utils.get_unique_file_path(f'predict_{round}_{conf_encoded}.slurm', slurm_case_dir )
        _info(f'creating: {slurm_file}')

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
        result = subprocess.run(cmd, shell=True)

        # Optionally check the result of the command
        if result.returncode == 0:
            print("Command executed successfully.")
        else:
            print(f"Command failed with return code {result.returncode}.")

    else: # run as a shell script

        sh_files_dir = config['sh_files_dir']

        script_file = utils.get_unique_file_path(f'predict_{round}_{conf_encoded}.sh', sh_files_dir )
        _info(f'creating: {script_file}')

        with open(script_file, 'w') as file:
            
            #switch to the base
            file.write(f'cd {nnunet_dir}\n')

            # export
            file.write(f'export nnUNet_raw="{raw_dir}"\n')
            file.write(f'export nnUNet_preprocessed="{preprocessed_dir}"\n')
            file.write(f'export nnUNet_results="{results_dir}"\n')
            
            file.write(cmd_lines)

        # sbatch
        import subprocess

        # Define the command
        cmd = f'chmod +x {script_file} && {script_file}'
        
        # Run the command and capture stdout and stderr
        result = subprocess.run(cmd, shell=True)

        # Optionally check the result of the command
        if result.returncode == 0:
            print("Command executed successfully.")
        else:
            print(f"Command failed with return code {result.returncode}.")


if __name__ == '__main__':

    dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART' 
    dataset_num = 103
    round = 'r2'
    folds = '0 1 2 3 4'
    plan = 'nnUNetPlans'
    trainer = 'nnUNetTrainer'
    use_slurm = False
    
    #dataset_name = 'Dataset009_Spleen'
    #dataset_num = 9

    #dataset_name = 'Dataset101_Eye[ul]L'
    #dataset_num = 101

    #dataset_name = 'Dataset102_ProneLumpStessin'
    #dataset_num = 102
    #for conf in ['3d_lowres']:
    for conf in ['3d_fullres']:
        postprocess(
            dataset_name=dataset_name,
            dataset_num=dataset_num,
            round = round,
            conf=conf,
            folds=folds,
            plan=plan,
            trainer=trainer,
            use_slurm=use_slurm
            )
    print('done')






