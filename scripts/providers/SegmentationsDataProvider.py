import requests

# this should be loaded from a config file
from config import get_config

class SegmentationsDataProvider():
    
    config = get_config()    
    if config['webservice_api_url'] != None:
        url = config['webservice_api_url']+'/segmentations'

    @staticmethod
    def get_all():
        r = requests.get(url = SegmentationsDataProvider.url)
        
        if r.status_code == 200:
            data = r.json()
        else:
            print("Error:", r.status_code)
        return data
    
    @staticmethod
    def get_one(_id):
        fn=f'SegmentationsDataProvider.get_one(_id={_id})'
        url = SegmentationsDataProvider.url+f'/{_id}'
        print(f'url={url}')
        r = requests.get(url)
        data = r.json()
        return data

    @staticmethod
    def add(obj):
        #print(obj)
        url = SegmentationsDataProvider.url
        #print(url)
        r = requests.post(url = url, json=obj)
        data = r.json()
        #print(data)
        return data

    @staticmethod
    def delete(id):
        #print(job)
        url = SegmentationsDataProvider.url+'/'+id
        #print(url)
        r = requests.delete(url = url)
        data = r.json()
        return data

    @staticmethod
    def update(obj):
        #print(job)
        url = SegmentationsDataProvider.url+'/'+obj['_id']
        #print(url)
        r = requests.put(url = url, json=obj)
        data = r.json()
        return data
        

    
