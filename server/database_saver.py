from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

""" _summary_ : fucntion take one news object and return id after saving object in mongoDB database
"""

def save_one_news(news_obj):
    # basic mongo Setup
    mongoURI = os.getenv('MONGO_URI')
    client = MongoClient(mongoURI)
    db = client.newsDB
    newsCollection = db.newsCollection

    # saving news object
    resp = newsCollection.insert_one(news_obj)
    return resp.inserted_id
