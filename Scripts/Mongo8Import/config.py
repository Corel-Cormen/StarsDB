import os
from pymongo import MongoClient

def get_connection():
    mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
    mongo_pass = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin123")
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_port = os.getenv("MONGO_PORT", "27018")
    mongo_db = os.getenv("MONGO_DB", "star_db")

    uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/"
    client = MongoClient(uri)
    db = client[mongo_db]
    return db
