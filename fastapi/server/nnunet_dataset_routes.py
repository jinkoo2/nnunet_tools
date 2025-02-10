from fastapi import APIRouter
import os

from pydantic import BaseModel


nnunet_data_dir = '/gpfs/projects/KimGroup/data/mic-mkfz'
nnunet_raw_dir =  os.path.join(nnunet_data_dir,'raw')
nnunet_preprocessed_dir =  os.path.join(nnunet_data_dir,'preprocessed')
nnunet_results_dir =  os.path.join(nnunet_data_dir,'results')

# Define the router
router = APIRouter()

from pathlib import Path
import re

def get_dataset_dirs(folder_path):
    """Get a list of data set."""
    pattern = r"^Dataset\d{3}_.+$"  # Regex for Datasetxxx_yyyyyy format
    return [entry.name for entry in Path(folder_path).iterdir() if entry.is_dir() and re.match(pattern, entry.name)]

@router.get("/dataset/list")
async def get_dataset_list():
    
    """Check the status of a task."""
    dirnames = get_dataset_dirs(nnunet_raw_dir)

    list = []    
    # read dataset.json files
    for dirname in dirnames:
        dir = os.path.join(nnunet_raw_dir, dirname)
        json_file = os.path.join(dir, 'dataset.json')
        try:
            with open(json_file, 'r') as f:
                import json
                data = json.load(f)
                data['id'] = dirname
                list.append(data)
        except Exception as e:
            print(f'Failed reading file {json_file}. Exception: {e}')

    print(list)

    return list

@router.get("/dataset/id-list")
async def get_dataset_list():
    
    """Get dataset is list"""
    ids = get_dataset_dirs(nnunet_raw_dir)

    return ids

class PlanAndPreprocessTaskRequest(BaseModel):
    dataset_num: int
    planner: str
    verify_dataset_integrity: bool

@router.post("/plan-and-preprocess/")
async def plan_and_preprocess(request: PlanAndPreprocessTaskRequest):
    """Submit a task for processing."""
    # Extract the `data` field from the TaskRequest object
    
    dataset_num = request.dataset_num
    planner = request.planner
    verify_dataset_integrity = request.verify_dataset_integrity

    print(f"dataset_num={dataset_num}")
    print(f"planner={planner}")
    print(f"verify_dataset_integrity={verify_dataset_integrity}")

    from nnunet_plan_and_preprocess import plan_and_preprocess_slurm
    print('RUNNING...plan_and_preprocess_slurm()')
    plan_and_preprocess_slurm(dataset_num, planner, verify_dataset_integrity)

    
