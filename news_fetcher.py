import requests
from dotenv import load_dotenv
import os
import json
import pprint

from database_saver import save_one_news
load_dotenv()


"""
[Summary] : function fetch news for india region
[Returns] : function return a list of news for india region, will return empty list if there are some issues at the moment

"""
def fetch_india_news():
    NEWS_URL = os.getenv('NEWS_DATA_API_URL')
    NEWS_API_KEY = os.getenv('NEWS_DATA_API_KEY')
    
    data = requests.get(url = NEWS_URL , params = {
        'apikey' : NEWS_API_KEY,
        'country' : 'IN'
    })
    data_json = data.json()
    if data_json['status'] == 'success':
        return data_json['results']
    else:
        return []


"""
[Summary] : function fetch news for Global region
[Returns] : function return a list of news for global region, will return empty list if there are some issues at the moment

"""
def fetch_global_news():
    NEWS_URL = os.getenv('NEWS_DATA_API_URL')
    NEWS_API_KEY = os.getenv('NEWS_DATA_API_KEY')
    
    data = requests.get(url = NEWS_URL , params = {
        'apikey' : NEWS_API_KEY
    })
    data_json = data.json()
    if data_json['status'] == 'success':
        return data_json['results']
    else:
        return []
