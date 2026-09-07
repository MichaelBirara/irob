from pymongo import MongoClient
from urllib.parse import urlparse

class MongoWriter:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        parsed = urlparse(connection_string)
        self.db_name = parsed.path.lstrip('/') or "irob_db"
        self.client = MongoClient(connection_string)
        self.db = self.client[self.db_name]

    def write(self, ir_data: dict):
        for collection_name, rows in ir_data.items():
            if not rows:
                continue
            collection = self.db[collection_name]
            collection.delete_many({}) # Clear existing or replace
            collection.insert_many(rows)
            print(f"Successfully wrote {len(rows)} documents to MongoDB collection '{collection_name}'.")
