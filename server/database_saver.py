from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def save_one_news(news_obj):
    # basic mongo Setup
    mongoURI = os.getenv('MONGO_URI')
    client = MongoClient(mongoURI)
    db = client.newsDB
    newsCollection = db.newsCollection

    # saving news object
    newsCollection.insert_one(news_obj)
