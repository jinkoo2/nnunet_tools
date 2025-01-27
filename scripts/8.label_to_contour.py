import os
from utils import _error, _info, _join_dir, _must_exist
from config import get_config

config = get_config()

def label_to_contour(
        labels_dir
    )->None:
    # convert a label image to contour.
    import image_helper

    _must_exist(labels_dir)

    for i, filename in enumerate(os.listdir(labels_dir)):

        if not filename.endswith('.mha'):
            continue

        seg_mha = f'{labels_dir}/{filename}'
        _must_exist(seg_mha)

        _info(f'[{i}] {os.path.basename(seg_mha)}')

        image_helper.seg_to_contour_list_json_files2(seg_mha=seg_mha)

if __name__ == '__main__':
    dataset_name = 'Dataset104_CBCTRectumBowel'
    round = 'r2'
    #conf = '2d'
    conf = '3d_lowres'
    #conf = '3d_fullres'
    raw_dir = config['raw_dir']
    conf_encoded = conf.replace('_', '[us]')
    postprocessed = False
    
    labels_dir = f'{raw_dir}/{dataset_name}/{round}_{conf_encoded}_predict'
    if postprocessed:
        labels_dir = os.path.join(labels_dir, 'pp')

    label_to_contour(labels_dir)