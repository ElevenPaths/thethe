from pymongo import MongoClient


class DB:
    def __init__(self, collection):
        self.client = MongoClient("mongodb://root:root@localhost:27017/")
        self.db = self.client.get_database("thethe")
        self.collection = self.db.get_collection(collection)

    def __del__(self):
        self.client.close()
