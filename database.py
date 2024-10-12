from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load MongoDB URI from .env file

client = MongoClient(os.getenv("MONGO_URI"))
db = client["fastapi_assignment"]
items_collection = db["items"]
clock_in_collection = db["clock_in"]
