import time
import json
import bson

from server.db import DB
from server.entities.resource_types import ResourceType
from server.entities.resource_base import ResourceBase
from server.entities.hash_types import HashType


class Hashes:
    db = DB("hash")

    @staticmethod
    def get_by_name(hash_string):
        hash_string = hash_string.lower()
        existing_hash = Hashes.db.collection.find_one({"hash": hash_string})
        if existing_hash:
            return Hash(existing_hash["_id"])

        else:
            hash_type = HashType.hash_detection(hash_string)

            if hash_type == HashType.UNKNOWN:
                raise Exception(f"Oops. Unknown hash type in Hash.py {hash_string}")
            args = {
                "hash": hash_string,
                "creation_time": time.time(),
                "hash_type": hash_type.value,
                "hash_short": hash_string[:8],
                "canonical_name": hash_string[:8],
                "resource_type": "hash",
                "plugins": [],
                "tags": [],
            }
            inserted_one = Hashes.db.collection.insert_one(args)

            return Hash(inserted_one.inserted_id)

    @staticmethod
    def get_by_id(resource_id):
        return Hash(resource_id)


class Hash(ResourceBase):
    def __init__(self, resource_id):
        super().__init__(resource_id, ResourceType.HASH)
