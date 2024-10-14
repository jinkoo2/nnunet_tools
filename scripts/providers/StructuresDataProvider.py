import requests
import os

# this should be loaded from a config file
from config import get_config

class StructuresDataProvider():
    
    config = get_config()
    if config['webservice_api_url'] != None:
        api_url = config['webservice_api_url']+'/structures'
        data_url = config['webservice_data_url']

    @staticmethod
    def get_all():
        r = requests.get(url = StructuresDataProvider.api_url)
        data = r.json()
        return data
    
    @staticmethod
    def get_filtered(filter):
      pass

    @staticmethod
    def get_one(id):
        r = requests.get(url = StructuresDataProvider.api_url+'/'+id)
        data = r.json()
        return data

    @staticmethod
    def add(obj):
        pass

    @staticmethod
    def delete(id):
        pass

    @staticmethod
    def update(obj):
        pass

    @staticmethod
    def download_file(url, out_file_path):
        res = requests.get(url)
        # Check if the request was successful (status code 200)
        if res.status_code == 200:
            with open(out_file_path, 'wb') as file:
                file.write(res.content)
            #print('File downloaded successfully.')
        else:
            msg = f'''Failed to download the file: {res.status_code}
                        url={url} 
                        out_file_path={out_file_path}'''
            print(msg)
            raise Exception(msg)

    @staticmethod
    def download_files(id, override=False):
        
        print('download_files for '+id)

        # get structure from db
        s = StructuresDataProvider.get_one(id)

        # download structure files (mhd, mha, info)
        str_mhd, str_files_downloaded = StructuresDataProvider.download_structure_files(s, override)
        
        # download image files (mhd, mha, info)
        img_mhd, img_files_downloaded = StructuresDataProvider.download_image_files(s, override)

        return {"structure_mhd": str_mhd, "structure_files_downloaded": str_files_downloaded, "image_mhd": img_mhd, "image_files_downloaded": img_files_downloaded}
    
    def download_structure_files(structure_object, override=False):
        
        s = structure_object

        file_downloaded = []

        # download to local folder
        dst_dir = StructuresDataProvider.config['structures_root_dir']+'/'+s['_id']
        print(f'dst_dir={dst_dir}')
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)    

        #mhd
        src_url = StructuresDataProvider.data_url+'/'+s['str_file_path']
        dst_file = dst_dir + '/img.mhd'
        if (override) or (not os.path.exists(dst_file)):
            StructuresDataProvider.download_file(src_url, dst_file)
            file_downloaded.append(dst_file)
        mhd = dst_file

        # Note: this is no longer needed to be done because we are using mha file
        # # rename the binary datafile to 'img.zraw'
        # p = Param()
        # p.load_from_txt(mhd)
        # p["ElementDataFile"] = "img.zraw"
        # p.save_to_txt(mhd)
        
        #mha
        src_url = src_url.replace('.mhd', '.mha')
        dst_file = dst_file.replace('.mhd', '.mha')
        if (override) or (not os.path.exists(dst_file)):
            StructuresDataProvider.download_file(src_url, dst_file)
            file_downloaded.append(dst_file)

        #info
        src_url = src_url.replace('.mha', '.info')
        dst_file = dst_file.replace('.mha', '.info')
        if (override) or (not os.path.exists(dst_file)):
            StructuresDataProvider.download_file(src_url, dst_file)
            file_downloaded.append(dst_file)

        return mhd, file_downloaded
    
    def download_image_files(structure_object, override=False):
        
        s = structure_object
        
        file_downloaded = []

        # download to local folder
        dst_dir = StructuresDataProvider.config['images_root_dir']+'/'+s['sset']['img']
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)    
        
        #mhd
        src_url = StructuresDataProvider.data_url+'/'+s['img_file_path']
        dst_file = dst_dir + '/img.mhd'
        if (override) or (not os.path.exists(dst_file)):
            StructuresDataProvider.download_file(src_url, dst_file)
            file_downloaded.append(dst_file)
        mhd = dst_file

        #mha
        src_url = src_url.replace('.mhd', '.mha')
        dst_file = dst_file.replace('.mhd', '.mha')
        if (override) or (not os.path.exists(dst_file)):
            StructuresDataProvider.download_file(src_url, dst_file)
            file_downloaded.append(dst_file)
        #info
        src_url = src_url.replace('img.mha', 'info.txt')
        dst_file = dst_file.replace('.mha', '.info')
        if (override) or (not os.path.exists(dst_file)):
            StructuresDataProvider.download_file(src_url, dst_file)
            file_downloaded.append(dst_file)

        return mhd, file_downloaded