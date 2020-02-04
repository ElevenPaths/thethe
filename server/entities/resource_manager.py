import bson
import re
import validators

from enum import Enum

from server.db import DB
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType, ResourceTypeException


class ResourceManager:
    @staticmethod
    def get(resource_id):
        """
            Return a resource by its ID.
            The resource must exists in database, otherwise use legacy db method
        """
        return Resource(resource_id)

    # TODO: "resource_type" should not be needed here, all resources must have a "searchable" field.
    @staticmethod
    def get_by_name(resource_name, resource_type):
        """
            Lookup database for a resource with name "resource_name"
            if None is found, then create the resource.
        """
        search = "canonical_name"
        resource_type = ResourceType.get_type_from_string(resource_type)

        if resource_type == ResourceType.HASH:
            search = "hash"

        db = Resource.collection()
        result = db.find_one({search: resource_name})
        if result:
            return Resource(result["_id"])

        # TODO: Legacy method for old database resources
        # TODO: Get rid of this legacy method
        if not result:
            docs = ["ip", "url", "username", "hash", "email", "domain"]
            for doc in docs:
                result = DB(doc).collection.find_one({search: resource_name})
                if result:
                    return Resource(result["_id"])

        print(f"Tried get_by_name nothing found {result}")
        return None

    @staticmethod
    def get_or_create(resource_name, resource_type):
        created = False
        resource = ResourceManager.get_by_name(resource_name, resource_type)
        if not resource:
            resource = Resource.create(resource_name, resource_type)
            created = True
        return (resource, created)

    @staticmethod
    def get_data_from_resources(resource_refs):
        result = []
        if not resource_refs:
            return result

        for resource_ref in resource_refs:
            resource = ResourceManager.get(resource_ref["resource_id"],)
            result.append(resource.get_data())

        return result
