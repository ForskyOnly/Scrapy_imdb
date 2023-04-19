from dotenv import load_dotenv
import os 
from pymongo import MongoClient


load_dotenv()

MONGODB_PWD = os.environ.get("MONGODB_PWD")

connection_todb = f"mongodb+srv://forskyonly:{MONGODB_PWD}@cluster1.rdzhoip.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_todb)


# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

dbs = client.list_database_names()
print(dbs)