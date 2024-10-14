import torch

print(f'torch.__version__={torch.__version__}')

# Check if GPUs are available
if torch.cuda.is_available():
    num_gpus = torch.cuda.device_count()
    print(f"Number of GPUs available: {num_gpus}")

    for i in range(num_gpus):
        gpu_name = torch.cuda.get_device_name(i)
        total_vram = torch.cuda.get_device_properties(i).total_memory / 1024**3  # Convert bytes to GB
        print(f"GPU {i}: {gpu_name}")
        print(f"  Total VRAM: {total_vram:.2f} GB")
else:
    print("No GPU available.")


print('done')