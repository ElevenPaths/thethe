import time
import json
import bson

from server.db import DB
from server.entities.resource_types import ResourceType
from server.entities.resource_base import ResourceBase


class Emails:
    db = DB("email")

    @staticmethod
    def get_by_name(email):
        existing_email = Emails.db.collection.find_one({"email": email})
        if existing_email:
            return Email(existing_email["_id"])

        else:
            args = {
                "canonical_name": email,
                "email": email,
                "creation_time": time.time(),
                "domain": email.split("@")[1],
                "plugins": [],
                "resource_type": "email",
                "tags": [],
            }
            inserted_one = Emails.db.collection.insert_one(args)

            return Email(inserted_one.inserted_id)

    @staticmethod
    def get_by_id(resource_id):
        return Email(resource_id)


class Email(ResourceBase):
    def __init__(self, resource_id):
        super().__init__(resource_id, ResourceType.EMAIL)
