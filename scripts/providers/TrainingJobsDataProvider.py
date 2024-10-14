import requests

# this should be loaded from a config file
from config import get_config

class TrainingJobsDataProvider():
    
    config = get_config()    
    if config['webservice_api_url'] != None and config['webservice_api_url'].strip() != '':
        url = config['webservice_api_url']+'/trainingjobs'

    @staticmethod
    def get_all():
        r = requests.get(url = TrainingJobsDataProvider.url)
        data = r.json()
        return data
    
    @staticmethod
    def get_jobs_not_completed():
        r = requests.get(url = TrainingJobsDataProvider.url+'/not_completed')
        data = r.json()
        return data

    @staticmethod
    def get_filtered(filter):
      pass

    @staticmethod
    def get_one(_id):
        fn=f'TrainingJobsDataProvider.get_one(_id={_id})'
        url = TrainingJobsDataProvider.url+f'/{_id}'
        print(f'url={url}')
        r = requests.get(url)
        data = r.json()
        return data

    @staticmethod
    def add(obj):
        #print(job)
        url = TrainingJobsDataProvider.url
        #print(url)
        r = requests.post(url = url, json=obj)
        data = r.json()
        return data

    @staticmethod
    def delete(id):
        #print(job)
        url = TrainingJobsDataProvider.url+'/'+id
        #print(url)
        r = requests.delete(url = url)
        data = r.json()
        return data

    @staticmethod
    def update(job):
        #print(job)
        url = TrainingJobsDataProvider.url+'/'+job['_id']
        #print(url)
        r = requests.put(url = url, json=job)
        data = r.json()
        return data
    
    @staticmethod
    def upload_file(job_id, file_path):
        #print('job_id=', job_id)
        #print('file_path=', file_path)
        url = TrainingJobsDataProvider.url+'/upload_file/'+job_id
        #print(url)
        
        files = {'file': open(file_path, 'rb')}
       
        try:
            response = requests.post(url = url, files=files)
            if response.status_code != 200:
                print(f"Error uploading file. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    
    @staticmethod
    def download_train_zip(job_id, out_file_path):
        url = TrainingJobsDataProvider.url+'/train_zip/'+job_id
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
    # @staticmethod
    # def update_properties(job_id, properties):
    #     #print(job)
    #     url = TrainingJobsDataProvider.url+'/'+job_id
    #     #print(url)
    #     r = requests.put(url = url, json=properties)
    #     data = r.json()
    #     return data
    
