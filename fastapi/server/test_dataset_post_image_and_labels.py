import requests
import os

url = "http://127.0.0.1:8000/dataset/add_image_and_labels"

script_dir = os.path.dirname(os.path.abspath(__file__))
print("Current script directory:", script_dir)

image_path = os.path.join(script_dir, "_test_images/base_image.mha")
labels_path = os.path.join(script_dir, "_test_images/labels.mha")

# Required metadata
dataset_id = "Dataset935_Test1"
images_for = "train"  # Must be "train" or "test"


# Open files safely using 'with' to avoid leaks
with open(image_path, "rb") as img_file, open(labels_path, "rb") as lbl_file:
    files = {
        "base_image": img_file,
        "labels": lbl_file,
    }
    data = {
        "dataset_id": dataset_id,
        "images_for": images_for,  # Renamed field
    }
    
    response = requests.post(url, files=files, data=data)

# Print response with error handling
if response.status_code == 200:
    print("Success:", response.json())
else:
    print(f"Error {response.status_code}: {response.text}")

