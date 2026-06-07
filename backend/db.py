from pymongo import MongoClient
from backend.config import MONGO_URI, DB_NAME

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DB_NAME]
