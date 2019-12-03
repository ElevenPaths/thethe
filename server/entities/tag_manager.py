import time
import json

from server.db import DB

AVAILABLE_COLORS = [
    "blue",
    "cyan",
    "green",
    "orange",
    "pink",
    "purple",
    "red",
    "yellow",
]


class TagManager:
    def __init__(self):
        self.db = DB("tags")

    def get_tags(self):
        results = self.db.collection.find({})
        return [result for result in results]

    def delete(self, name):
        self.db.collection.delete_one({"name": name})

    def new(self, tag):
        tag["name"] = tag["name"].lower()

        if not tag["name"].isalnum():
            return None

        if not tag["color"] in AVAILABLE_COLORS:
            return None

        if not self.db.collection.find_one({"name": tag["name"]}):
            self.db.collection.insert_one({"name": tag["name"], "color": tag["color"]})
        else:
            return None

    def update(self, old_name, new_tag):
        self.db.collection.update_one(
            {"name": old_name}, {"name": new_tag["name"], "color": new_tag["color"]}
        )
