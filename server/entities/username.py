import time
import json
import bson

from server.db import DB
from server.entities.resource_types import ResourceType
from server.entities.resource_base import ResourceBase


class Usernames:
    db = DB("username")

    @staticmethod
    def get_by_name(username):
        existing_username = Usernames.db.collection.find_one({"username": username})
        if existing_username:
            return Username(existing_username["_id"])

        else:
            args = {
                "canonical_name": username,
                "username": username,
                "creation_time": time.time(),
                "plugins": [],
                "resource_type": "username",
                "tags": [],
                "sites": [],
            }
            inserted_one = Usernames.db.collection.insert_one(args)

            return Username(inserted_one.inserted_id)

    @staticmethod
    def get_by_id(resource_id):
        return Username(resource_id)


class Username(ResourceBase):
    def __init__(self, resource_id):
        super().__init__(resource_id, ResourceType.USERNAME)
