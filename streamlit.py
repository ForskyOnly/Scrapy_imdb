
import streamlit
from dotenv import load_dotenv
import os 
import pymongo
from pymongo.mongo_client import MongoClient



load_dotenv("/home/apprenant/Documents/01projet_python/DevIA_Roubaix/scrapy/test/series250/.env")

MONGODB_PWD = os.environ.get("MONGODB_PWD")
MANGODB_PSEUDO = os.environ.get("MANGODB_PSEUDO")
MANGODB_PSEUDO

connection_todb = f"mongodb+srv://forskyonly:{MONGODB_PWD}@cluster1.rdzhoip.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_todb)
db = client["imdb_data"]
collection = db["films_series"]
