from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json
import random
import os
import re


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

    list = sorted(list, key=lambda x: x["id"])

    print(list)

    return list

@router.get("/dataset/id-list")
async def get_dataset_id_list():
    
    """Get dataset is list"""
    ids = get_dataset_dirs(nnunet_raw_dir)

    return ids


class DatasetRequest(BaseModel):
    """Pydantic model for dataset validation."""
    name: str
    description: str
    reference: str
    licence: str
    tensorImageSize: str
    labels: dict
    channel_names: dict

@router.post("/dataset/new")
async def post_dataset(request: Request):
    """Create a new dataset with validation."""
    try:
        data = await request.json()  # Extract JSON body
        print(f"Received dataset: {json.dumps(data, indent=4)}")

        # **Validation 1: Required fields**
        required_fields = ["name", "description", "reference", "licence", "tensorImageSize", "labels", "channel_names","file_ending"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        # **Validation 2: Check if "name" is alphanumeric without spaces**
        if not data["name"].isalnum():
            raise HTTPException(status_code=400, detail="Error: 'name' must be alphanumeric and contain no spaces.")

        # **Validation 3: Check if "tensorImageSize" is either "2D" or "3D"**
        if data["tensorImageSize"] not in ["2D", "3D"]:
            raise HTTPException(status_code=400, detail="Error: 'tensorImageSize' must be either '2D' or '3D'.")

        # **Validation 4: Ensure "labels" contains "background" with value 0**
        if "background" not in data["labels"] or data["labels"]["background"] != 0:
            raise HTTPException(status_code=400, detail="Error: 'labels' must include 'background' with value 0.")

        # **Set default values if not present**
        data.setdefault("numTraining", 0)
        data.setdefault("numTest", 0)

        # **Find all used dataset numbers**
        # **Find all used dataset numbers and names**
        existing_datasets = get_dataset_dirs(nnunet_raw_dir)
        used_numbers = set()
        existing_names = set()

        for dataset in existing_datasets:
            match = re.match(r"Dataset(\d{3})_(.+)$", dataset)
            if match:
                used_numbers.add(int(match.group(1)))
                existing_names.add(match.group(2))

        print(f"🔢 Used dataset numbers: {used_numbers}")
        print(f"📂 Existing dataset names: {existing_names}")

        # **Check if the dataset name is already in use**
        if data["name"] in existing_names:
            raise HTTPException(status_code=400, detail=f"Error: Dataset name '{data['name']}' already exists.")
    
        # **Generate a random unused dataset number**
        available_numbers = set(range(1, 1000)) - used_numbers  # Numbers 1-999 not in use
        if not available_numbers:
            raise HTTPException(status_code=500, detail="Error: No available dataset numbers left.")

        new_dataset_num = random.choice(list(available_numbers))

        print(f'new_dataset_num={new_dataset_num}')

        # **Generate new dataset ID**
        dataset_id = f"Dataset{new_dataset_num:03d}_{data['name']}"
        dataset_path = os.path.join(nnunet_raw_dir, dataset_id)

        print(f'dataset_path={dataset_path}')

        # **Create new dataset directory and save dataset.json**
        os.makedirs(dataset_path, exist_ok=True)
        json_path = os.path.join(dataset_path, "dataset.json")
        print(f'json_path={json_path}')

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)

        data["id"] = dataset_id

        return {
            "message": "Dataset successfully created!",
            "dataset": data
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format. Please send valid JSON.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    


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

    
