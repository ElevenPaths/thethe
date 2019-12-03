import time
import hashlib
import base64

from server.db import DB


class Paste:
    def __init__(self, paste_key, meta):
        # From googlesearch
        self.paste_key = paste_key
        # Own
        ts = time.time()
        self.creation_time = ts
        self.update_time = ts
        self.not_found = False
        self.md5 = None
        # Meta
        self.size = meta["size"]
        self.title = meta["title"]
        self.user = meta["user"]
        self.hits = meta["hits"]
        self.date = meta["date"]
        self.syntax = meta["syntax"]
        self.expire = meta["expire"]
        # Raw
        self.content = None

    def set_content(self, content):
        md5 = hashlib.md5()
        md5.update(content)
        self.md5 = md5.hexdigest()
        self.content = content

    def save(self):
        previous = DB("pastebins").collection.find_one({"paste_key": self.paste_key})
        if not previous:
            if not self.md5:
                self.not_found = True
            result = DB("pastebins").collection.insert_one(self.__dict__)
            return result.inserted_id
        else:
            return previous["_id"]


class PastebinManager:
    def __init__(self):
        self.db = DB("pastebins")

    def get(self, paste_key):
        return self.db.collection.find_one({"paste_key": paste_key})

    def get_by_id(self, _id):
        return self.db.collection.find_one({"_id": _id})

    def delete(self, paste_key):
        self.db.collection.delete_one({"paste_key": paste_key})

    def new(self, paste_obj):
        if not self.get(paste_obj["paste_key"]):
            paste_obj["creation_time"] = time.time()
            paste_obj["update_time"] = time.time()
            self.db.collection.insert_one(paste_obj)

    def update(self, paste_key):
        self.db.collection.update_one(
            {"paste_key": paste_key}, {"update_time": time.time()}
        )
