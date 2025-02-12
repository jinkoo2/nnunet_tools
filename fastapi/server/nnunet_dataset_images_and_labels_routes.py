from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from pathlib import Path
import os
import json
import shutil

# FastAPI Router
router = APIRouter()

# Config and paths
from config import get_config
nnunet_data_dir = get_config()["data_dir"] 
nnunet_raw_dir = os.path.join(nnunet_data_dir, 'raw')

@router.post("/dataset/add_image_and_labels")
async def add_image_and_labels(
    dataset_id: str = Form(...),
    images_for: str = Form(...),  # "train" or "test"
    base_image: UploadFile = File(...),
    labels: UploadFile = File(...)
):
    """
    Uploads a base image and label mask to the correct dataset folder.

    - `dataset_id`: Name of the dataset (e.g., "Dataset001_Sample").
    - `images_for`: "train" or "test".
    - `base_image`: The main CT scan image.
    - `labels`: The corresponding label mask.
    """
    # Validate dataset directory
    dataset_path = os.path.join(nnunet_raw_dir, dataset_id)
    dataset_json_path = os.path.join(dataset_path, "dataset.json")
    
    if not os.path.exists(dataset_path) or not os.path.exists(dataset_json_path):
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found.")
    
    # Load dataset.json
    try:
        with open(dataset_json_path, "r") as f:
            dataset_info = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read dataset.json: {str(e)}")
    
    # Validate required keys in dataset.json
    required_keys = ["numTraining", "numTest", "file_ending"]
    for key in required_keys:
        if key not in dataset_info:
            raise HTTPException(status_code=400, detail=f"Missing key '{key}' in dataset.json")

    file_ending = dataset_info["file_ending"]  # Example: ".nii.gz"

    # Determine target folders and naming
    if images_for == "train":
        num = dataset_info["numTraining"]
        images_folder = os.path.join(dataset_path, "imagesTr")
        labels_folder = os.path.join(dataset_path, "labelsTr")
        dataset_info["numTraining"] += 1  # Increment counter
    elif images_for == "test":
        num = dataset_info["numTest"]
        images_folder = os.path.join(dataset_path, "imagesTs")
        labels_folder = os.path.join(dataset_path, "labelsTs")
        dataset_info["numTest"] += 1  # Increment counter
    else:
        raise HTTPException(status_code=400, detail="Invalid images_for value. Must be 'train' or 'test'.")

    # Ensure target directories exist
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(labels_folder, exist_ok=True)

    # Construct filenames
    base_image_filename = f"image_{num}_0000{file_ending}"
    labels_filename = f"labels_{num}{file_ending}"

    base_image_path = os.path.join(images_folder, base_image_filename)
    labels_path = os.path.join(labels_folder, labels_filename)

    # Save files
    try:
        with open(base_image_path, "wb") as buffer:
            shutil.copyfileobj(base_image.file, buffer)
        
        with open(labels_path, "wb") as buffer:
            shutil.copyfileobj(labels.file, buffer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save images: {str(e)}")

    # Save updated dataset.json
    try:
        with open(dataset_json_path, "w") as f:
            json.dump(dataset_info, f, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update dataset.json: {str(e)}")

    if "id" not in dataset_info:
        dataset_info['id'] = dataset_id
        
    return dataset_info  # Return updated dataset.json
