import time
import json
import bson
import urllib.parse

from server.db import DB
from server.entities.resource_types import ResourceType
from server.entities.resource_base import ResourceBase


class URLs:
    db = DB("url")

    @staticmethod
    def get_by_name(url):
        previous_url = URLs.db.collection.find_one({"full_url": url})
        if previous_url:
            return URL(previous_url["_id"])

        else:
            url_parts = urllib.parse.urlparse(url)

            args = {
                "canonical_name": url,
                "resource_type": "url",
                "scheme": url_parts.scheme,
                "netloc": url_parts.netloc,
                "path": url_parts.path,
                "params": url_parts.params,
                "query": url_parts.query,
                "fragment": url_parts.fragment,
                "full_url": url,
                "creation_time": time.time(),
                "plugins": [],
                "tags": [],
            }

            inserted_one = URLs.db.collection.insert_one(args)

            return URL(inserted_one.inserted_id)

    @staticmethod
    def get_by_id(resource_id):
        return URL(resource_id)


class URL(ResourceBase):
    def __init__(self, resource_id):
        super().__init__(resource_id, ResourceType.URL)
