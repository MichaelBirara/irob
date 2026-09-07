from pymongo import MongoClient
from urllib.parse import urlparse

class MongoReader:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        parsed = urlparse(connection_string)
        self.db_name = parsed.path.lstrip('/') or "irob_db"
        self.client = MongoClient(connection_string)
        self.db = self.client[self.db_name]

    def read(self) -> dict:
        collections = self.db.list_collection_names()
        ir_data = {}
        for col in collections:
            docs = list(self.db[col].find({}, {"_id": 0}))
            ir_data[col] = docs
        return ir_data
