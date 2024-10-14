echo "loadign pytorch module"
module load pytorch-gpu/2.0.1 
python --version
pip --version 

echo "creating a viritual environment, and activate it"
python -m venv /gpfs/scratch/jinkokim/venv_list/nnunet
source /gpfs/scratch/jinkokim/venv_list/nnunet/bin/activate

echo "download source code from github, and install the dependent packages"
module load git
mkdir src
cd src
git clone https://github.com/jinkoo2/nnUNet.git .
pip install -e .

echo "optional hiddenlayer for model plot"
pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git

export nnUNet_raw="/gpfs/projects/KimGroup/data/mic-mkfz/raw"
export nnUNet_preprocessed="/gpfs/projects/KimGroup/data/mic-mkfz/preprocessed"
export nnUNet_results="/gpfs/projects/KimGroup/data/mic-mkfz/results"

nvidia-smi




