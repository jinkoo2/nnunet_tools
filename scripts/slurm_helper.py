import subprocess


import subprocess
import json


def _run(cmd):
    return subprocess.run(f"module load slurm && {cmd}", shell=True, capture_output=True, text=True)

def get_my_job_ids(userid):

    # Run the squeue command to get job IDs for the specified user
    result = _run(f"squeue -u {userid} -h -o %i")
    
    # Check if there was an error running the command
    if result.returncode != 0:
        print(f"Error executing squeue: {result.stderr}")
        return []

    # Split the output by newlines and remove empty strings (in case there are no jobs)
    job_ids = [job_id for job_id in result.stdout.strip().split("\n") if job_id]
    
    return job_ids
    
def get_job_info(job_id):
    # Run the `scontrol show job <job_id>` command
    result = _run(f"scontrol show job {job_id}")

    if result.returncode != 0:
        print(result.stderr)
        return None
    
    # Split the output into lines and then into key-value pairs
    job_info_lines = result.stdout.strip().split("\n")
    
    job_info_dict = {}
    for line in job_info_lines:
        # The output might contain fields separated by spaces, so we replace '=' and split by spaces
        for field in line.split():
            if "=" in field:
                key, value = field.split("=", 1)
                job_info_dict[key] = value

    return job_info_dict


def suspend_job(job_id):
    # Run the `scontrol show job <job_id>` command
    result = _run(f"scontrol suspend {job_id}")

    return result

def resume_job(job_id):
    result = _run(f"scontrol resume {job_id}")
    return result

def cancel_job(job_id):
    result = _run(f"scancel {job_id}")
    return result

def save_job_info_to_json(job_id, filename):
    # Get job information
    job_info = get_job_info(job_id)

    # Save job info to JSON file
    with open(filename, 'w') as json_file:
        json.dump(job_info, json_file, indent=4)

def print_my_job_state(userid):
    job_ids = get_my_job_ids(userid)
    for job_id in job_ids:
        job = get_job_info(job_id)
        print(f'{job_id}->{job["JobState"]}')


def get_my_first_running_job(userid):
    job_ids = get_my_job_ids(userid)
    for job_id in job_ids:
        job = get_job_info(job_id)
        if job["JobState"] == 'RUNNING':
            return job
    return None

def cancel_my_all_jobs(userid):
    job_ids = get_my_job_ids(userid)
    for job_id in job_ids:
        print(f'caceling job: {job_id}')
        cancel_job(job_id)

if __name__ == '__main__':
    userid = 'jinkokim'
   
    print_my_job_state(userid)
    
    print('done')
