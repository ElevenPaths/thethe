import time
import json
import bson

from server.db import DB
from server.entities.resource_types import ResourceType
from server.entities.resource_base import ResourceBase


class Domains:
    db = DB("domain")

    @staticmethod
    def get_by_name(domain_name):
        domain_exists = Domains.db.collection.find_one({"domain": domain_name})
        if domain_exists:
            return Domain(domain_exists["_id"])

        else:
            args = {
                "canonical_name": domain_name,
                "domain": domain_name,
                "creation_time": time.time(),
                "plugins": [],
                "resource_type": "domain",
                "tags": [],
            }
            inserted_one = Domains.db.collection.insert_one(args)

            return Domain(inserted_one.inserted_id)

    @staticmethod
    def get_by_id(resource_id):
        return Domain(resource_id)


class Domain(ResourceBase):
    def __init__(self, resource_id):
        super().__init__(resource_id, ResourceType.DOMAIN)
