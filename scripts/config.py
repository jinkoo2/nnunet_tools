import os

#################
# ENV load .env file
from dotenv import load_dotenv
load_dotenv()

def get_config():
   
    data_root_dir = 'd:/projects/progressive_segmentation_framework/seg_worker/__data'
    data_root_dir = os.getenv('data_root_dir')
    if data_root_dir==None:
        raise Exception(f'Error: "data_root_dir" is not found in the environment')
    
    if not os.path.exists(data_root_dir):
        print(f'making data_root_dir: {data_root_dir}')
        os.makedirs(data_root_dir)

    structures_root_dir = os.path.join(data_root_dir,'structures')
    images_root_dir = os.path.join(data_root_dir,'images')
    jobs_root_dir = os.path.join(data_root_dir,'jobs')

    webservice_api_url= os.getenv('webservice_api_url')
    webservice_data_url= os.getenv('webservice_data_url')

    ret = {
        'webservice_available': webservice_api_url != None,
        'webservice_api_url': webservice_api_url,
        'webservice_data_url': webservice_data_url,
        'data_root_dir': data_root_dir,
        'structures_root_dir' : structures_root_dir,
        'images_root_dir': images_root_dir,
        'jobs_root_dir' : jobs_root_dir,
    }

    #print('get_config().return=', ret)

    return ret
