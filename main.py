from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data

file_path = './data/spotify_history.csv'
df = extract_data(file_path)
df = transform_data(df)
load_data(df)

# import datetime
# import uuid
# from pymongo import MongoClient
# from bson.objectid import ObjectId

# # create client
# client = MongoClient("localhost", 27017)

# # get/create database
# db = client.ktechhub
# # db = client.ktech_hub ##this works
# # db = client['ktech-hub'] ##this works
# print(client.list_database_names())

# # create/get collection
# collection = db.posts
# print(db.list_collection_names())
