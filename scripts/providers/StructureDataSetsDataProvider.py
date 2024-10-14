import requests
import os

# this should be loaded from a config file
from config import get_config

class StructureDataSetsDataProvider():
    
    config = get_config()
    if config['webservice_api_url'] != None:
        api_url = config['webservice_api_url']+'/structuredatasets'
        data_url = config['webservice_data_url']

    @staticmethod
    def get_all():
        r = requests.get(url = StructureDataSetsDataProvider.api_url)
        data = r.json()
        return data
    
    @staticmethod
    def get_filtered(filter):
      pass

    @staticmethod
    def get_one(id):
        r = requests.get(url = StructureDataSetsDataProvider.api_url+'/'+id)
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

