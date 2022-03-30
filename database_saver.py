from calendar import c

from matplotlib.style import available
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
    print("Saved in database with id : " + str(resp.inserted_id))
    return resp.inserted_id

"""
    News_tag_Schema : {
        news_tag : {
            name : "sports"
            articles : ['id']
        }
    }
    
"""
def insert_tags(news_id : str , news_tags : list):
    # basic mongo setup
    mongoURI = os.getenv('MONGO_URI')
    client = MongoClient(mongoURI)
    db = client.newsDB
    tagCollection = db.tagCollection
    
    # inserting tag for first time starts here
    availableTags = tagCollection.find({"name" : {"$in" : news_tags}})
    available_tag_list = []
    for tag in availableTags:
        available_tag_list.append(tag['name'])
    
    new_tags = []
    
    for tag in news_tags:
        if tag in available_tag_list:
            continue
        else:
            new_tags.append({'name' : tag , 'articles' : []})
    # query to update tags array list
    if(len(new_tags) > 0):
        tagCollection.insert_many(new_tags)

    # inserting tag for first time ends here
    
    # updating all tags with news_id
    tagCollection.update_many(
        {"name" : {"$in" : news_tags}},
        {'$push' : {"articles" : news_id}}
    )
    
    # done

