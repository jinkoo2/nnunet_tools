import os
from providers.StructureDataSetsDataProvider import StructureDataSetsDataProvider
from providers.StructuresDataProvider import StructuresDataProvider

#dataset_num = 101
#data_id = '64b054558c9e5d2ca292410d' # Eye_L
#desc = 'small test dataset'

dataset_num = 102
data_id = '658b5bd841a86da715a6ce0b' # ProneLumpStessin
desc = 'Prone Lumpectomy Contours for Dr. Stessin'


dataset_num = 103
data_id = '66747c610028ad1b5c145f0f' # CBCT Bladder
desc = 'CBCTBladderART'

ds = StructureDataSetsDataProvider.get_one(data_id)
print('Name=', ds['Name'])


sids_train = [ s['_id'] for s in ds['TrainSet']]
sids_valid = [ s['_id'] for s in ds['ValidSet']]
sids_test = [ s['_id'] for s in ds['TestSet']]

# combine valid to trainset
sids_train = sids_train + sids_valid

def download_s_files(sids):
    image_pair_list=[]
    for sid in sids:
        try:
            download = StructuresDataProvider.download_files(sid)
            image_file = download['image_mhd'].replace('.mhd', '.mha')
            label_file = download['structure_mhd'].replace('.mhd', '.mha')
            image_pair = {'image_file':image_file, 'label_file':label_file}
            image_pair_list.append(image_pair)
        except Exception as e:
            print(e)

    return image_pair_list

def _join_dir(path1, path2):
    path3 = os.path.join(path1, path2)
    if not os.path.exists(path3):
        os.makedirs(path3)
    return path3
    
nnUNet_data_dir = '/gpfs/projects/KimGroup/data/mic-mkfz'
nnUNet_raw_dir = os.path.join(nnUNet_data_dir, 'raw')


dataset_name = ds['Name'].replace(' ', '[sp]').replace('_','[ul]')

dataset_dirname = f'Dataset{dataset_num:03}_{dataset_name}'
dataset_dir =  _join_dir(nnUNet_raw_dir, dataset_dirname)
print(f'dataset_dir={dataset_dir}')

imagesTr = _join_dir(dataset_dir, 'imagesTr')
labelsTr = _join_dir(dataset_dir, 'labelsTr')
imagesTs = _join_dir(dataset_dir, 'imagesTs')
labelsTs = _join_dir(dataset_dir, 'labelsTs')

train_list = download_s_files(sids_train)
test_list = download_s_files(sids_test)

def add_index(obj_list):
    for index, obj in enumerate(obj_list):
        obj['i'] = index

from param import Param

def get_image_prop(mhd_file):
    p = Param()
    p.load_from_txt(mhd_file)
    size = p.get_item_as_int_array('DimSize', ' ')
    direction = p.get_item_as_float_array('TransformMatrix', ' ')
    origin = p.get_item_as_float_array('Offset', ' ')
    spacing = p.get_item_as_float_array('ElementSpacing', ' ')
    return {
        'size': size,
        'direction' : direction,
        'origin' : origin,
        'spacing': spacing
    }

def list_eq(list1, list2):
    if len(list1) != len(list2):
        return False
    
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False

    return True

def compare_image_props(prop1, prop2):
    size_eq = list_eq(prop1['size'], prop2['size'])
    spacing_eq = list_eq(prop1['spacing'], prop2['spacing'])
    direction_eq = list_eq(prop1['direction'], prop2['direction'])
    origin_eq = list_eq(prop1['origin'], prop2['origin'])

    eq = size_eq and spacing_eq and direction_eq and origin_eq

    return {
            'eq': eq, 
            'size_eq': size_eq,
            'spacing_eq': spacing_eq,
            'direction_eq': direction_eq,
            'origin_eq': origin_eq
    }

def get_image_pairs_of_equal_props(pair_list):
    list_eq = []
    list_not_eq = []
    for index, pair in enumerate(pair_list):
        if pair['prop_comparison']['eq']:
            list_eq.append(pair)
        else:
            list_not_eq.append(pair)
        
    return list_eq, list_not_eq


def add_img_prop(pair_list):
    for index, pair in enumerate(pair_list):
        image_mhd = pair['image_file'].replace('.mha', '.mhd')
        image_prop = get_image_prop(image_mhd)
        
        
        label_mhd = pair['label_file'].replace('.mha', '.mhd')
        label_prop = get_image_prop(label_mhd)

        pair['image_prop'] = image_prop
        pair['label_prop'] = label_prop

        comp = compare_image_props(image_prop, label_prop)
        pair['prop_comparison'] = comp

add_index(train_list)
add_img_prop(train_list)
train_list, train_list_excluded = get_image_pairs_of_equal_props(train_list)

add_index(test_list)
add_img_prop(test_list)
test_list, test_list_excluded = get_image_pairs_of_equal_props(test_list)

import json

download = {'train_list': train_list, 'test_list': test_list}
downloaded_pair_list_file = os.path.join(dataset_dir, 'downloaded_files.json')
with open(downloaded_pair_list_file, 'w') as f:
    json.dump(download, f, indent=4)

downloaded_but_excluded = {'train_list': train_list_excluded, 'test_list': test_list_excluded}
downloaded_but_excluded_pair_list_file = os.path.join(dataset_dir, 'downloaded_but_excluded_files.json')
with open(downloaded_but_excluded_pair_list_file, 'w') as f:
    json.dump(downloaded_but_excluded, f, indent=4)


# cp the image to nnUNet data folder
import shutil

def copy_image_pair_list(pair_list, dst_images_dir, dst_labels_dir, start_index):
    i = start_index
    for pair in pair_list:
        image_file_src = pair['image_file']
        label_file_src = pair['label_file']

        image_filename_dst = f'{dataset_name.lower()}_{i}_0000.mha'
        label_filename_dst = f'{dataset_name.lower()}_{i}.mha'
        
        image_file_dst = os.path.join(dst_images_dir, image_filename_dst)
        label_file_dst = os.path.join(dst_labels_dir, label_filename_dst)

        shutil.copy(image_file_src, image_file_dst)
        shutil.copy(label_file_src, label_file_dst)
        i+=1
    return i

i=0
i = copy_image_pair_list(train_list, imagesTr, labelsTr, i)
i = copy_image_pair_list(test_list, imagesTs, labelsTs, i)

import json

info = {
    "name": dataset_name,
    "description": desc,
    "reference": "Stony Brook Univ Hospital",
    "licence": "CC-BY-SA 4.0",
    "release": "1.0 08/28/2024",
    "tensorImageSize": "3D",
    "labels": {
        "background": 0,
        "eye[ul]l": 1
    },
    "numTraining": len(train_list),
    "numTest": len(test_list),
    "file_ending": ".mha",
    "channel_names": {
        "0": "CT"
    }
 }

dataset_json_file = os.path.join(dataset_dir, 'dataset.json')
with open(dataset_json_file, 'w') as json_file:
    json.dump(info, json_file, indent=4)

print('done')
