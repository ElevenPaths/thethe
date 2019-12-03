import time
import json
import bson

from server.db import DB
from server.entities.resource_types import ResourceType
from server.entities.resource_base import ResourceBase


class IPs:
    db = DB("ip")

    @staticmethod
    def get_by_name(ip_address):
        if ":" in ip_address:
            ip_address = ip_address.split(":")[0]

        ip = IPs.db.collection.find_one({"address": ip_address})
        if ip:
            return IP(ip["_id"])

        else:
            args = {
                "canonical_name": ip_address,
                "resource_type": "ip",
                "address": ip_address,
                "creation_time": time.time(),
                "plugins": [],
                "tags": [],
            }

            inserted_one = IPs.db.collection.insert_one(args)

            return IP(inserted_one.inserted_id)

    @staticmethod
    def get_by_id(resource_id):
        return IP(resource_id)


class IP(ResourceBase):
    def __init__(self, resource_id):
        super().__init__(resource_id, ResourceType.IPv4)
