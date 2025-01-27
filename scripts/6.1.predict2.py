
import os
from utils import _error, _info, _join_dir, _must_exist, get_current_datetime_str, copy_file_to_folder
import utils
from config import get_config


def predict(
        dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART', 
        dataset_num = 103,
        round = 'r2',
        conf = '3d_lowres',
        folds = '0 1 2 3 4',
        plan = 'nnUNetPlans',
        trainer = 'nnUNetTrainer',
        use_slurm = True,
        device = 'cuda', 
        run_after_slurm_job_id=None
        )->None:

    config = get_config()
        
    scripts_dir = config['scripts_dir']
    nnunet_dir = config['nnunet_dir']
    data_dir = config['data_dir']

    raw_dir = config['raw_dir']
    preprocessed_dir= config['preprocessed_dir']
    results_dir = config['results_dir']

    slurm_files_dir = config['slurm_files_dir']

    conf_encoded = conf.replace('_', '[us]')

    dataset_results_dir = _join_dir(results_dir, dataset_name)

    imagesTs_dir = os.path.join(os.path.join(raw_dir, dataset_name), f'{round}_imagesTs')
    labelsTs_predict = os.path.join(os.path.join(raw_dir, dataset_name), f'{round}_{conf_encoded}_predict')
    #labelsTs_predict_pp = os.path.join(labelsTs_predict, 'pp')

    # copy only those not complated to a new input folder
    if os.path.exists(labelsTs_predict):
        result_file_count = len(os.listdir(labelsTs_predict))
        if result_file_count > 0:
            _info(f'the desination folder already has {result_file_count}. so exluding already completed input images...')
            
            new_imagesTs_dir = f'{imagesTs_dir}_{get_current_datetime_str()}'
            os.makedirs(new_imagesTs_dir)

            input_filenames = os.listdir(imagesTs_dir)
            for input_filename in input_filenames:
                if not input_filename.endswith('.mha'):
                    continue

                input_file = os.path.join(imagesTs_dir, input_filename)
                output_filename = input_filename.replace('_0000.mha', '.mha')
                output_file = os.path.join(labelsTs_predict, output_filename)

                if not os.path.exists(output_file):
                    copy_file_to_folder(source_file=input_file, destination_folder=new_imagesTs_dir)

            imagesTs_dir = new_imagesTs_dir

    # predition
    pred_i = imagesTs_dir
    pred_o = labelsTs_predict
    pred_f = folds 
    pred_tr = trainer
    pred_c = conf
    pred_p = plan
    pred_d = device 
    pred_cmd = f'nnUNetv2_predict -d {dataset_name} -i {pred_i} -o {pred_o} -f  {pred_f} -tr {pred_tr}  -c {pred_c} -p {pred_p} -device {pred_d}\n'
    _info(pred_cmd)

    _must_exist(pred_i)

    # post processing
    #pp_i =  pred_o  
    #pp_o = labelsTs_predict_pp
    #folds_str = pred_f.replace(' ', '_')
    #cross_val_results_dir = f'{dataset_results_dir}/{pred_tr}__{pred_p}__{pred_c}/crossval_results_folds_{folds_str}'
    #pp_pkl_file=f'{cross_val_results_dir}/postprocessing.pkl'
    #pp_np=8
    #pp_plans_json=f'{cross_val_results_dir}/plans.json'
    #pp_cmd = f'nnUNetv2_apply_postprocessing -i {pp_i} -o {pp_o} -pp_pkl_file {pp_pkl_file} -np {pp_np} -plans_json {pp_plans_json}\n'
    #_info(pp_cmd)

    #_must_exist(cross_val_results_dir)
    #_must_exist(pp_pkl_file)
    #_must_exist(pp_plans_json)

    cmd_lines = f'{pred_cmd}\n'

    if use_slurm:

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

                
        if run_after_slurm_job_id == None:
            cmd = f'module load slurm && sbatch {slurm_file}'
        else:
            cmd = f'module load slurm && sbatch --dependency=afterany:{run_after_slurm_job_id} {slurm_file}'

        print(f'running "{cmd}"')
        subprocess.run(cmd, shell=True)

    else: # run as a shell script
        script_file = os.path.join(dataset_results_dir, 'predict.sh')
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

        cmd = f'chmod +x {script_file} && {script_file}'
        print(f'running "{cmd}"')
        subprocess.run(cmd, shell=True)

if __name__ == '__main__':

    #dataset_name = 'Dataset103_CBCT[sp]Bladders[sp]For[sp]ART' 
    #dataset_num = 103
    dataset_name = 'Dataset104_CBCTRectumBowel' 
    dataset_num = 104
    round = 'r2'
    folds = '0 1 2 3 4'
    plan = 'nnUNetPlans'
    trainer = 'nnUNetTrainer'
    use_slurm = True
    device = 'cuda'

       
    #dataset_name = 'Dataset009_Spleen'
    #dataset_num = 9

    #dataset_name = 'Dataset101_Eye[ul]L'
    #dataset_num = 101

    #dataset_name = 'Dataset102_ProneLumpStessin'
    #dataset_num = 102
    for conf in ['3d_lowres']:
    #for conf in ['3d_fullres']:
        predict(
            dataset_name=dataset_name,
            dataset_num=dataset_num,
            round = round,
            conf=conf,
            folds=folds,
            plan=plan,
            trainer=trainer,
            use_slurm=use_slurm,
            device=device
            )
    print('done')






