from pymongo import MongoClient
from bson.objectid import ObjectId
import os

class Database:
    def __init__(self):
        # Fix environment variable names to match docker-compose
        mongo_uri = os.getenv("MONGO_URL", "mongodb://admin:password@mongo:27017/flowbit?authSource=admin")
        db_name = os.getenv("MONGO_DB_NAME", "flowbit")
        
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()

# Global database instance
db = Database()