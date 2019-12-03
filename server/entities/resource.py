import bson
import re
import validators

from enum import Enum

from server.db import DB
from server.utils.validations import HashType, hash_detection

from server.entities.ip import IPs
from server.entities.domain import Domains
from server.entities.email import Emails
from server.entities.hash import Hashes
from server.entities.url import URLs
from server.entities.username import Usernames

from server.entities.resource_types import ResourceType, ResourceTypeException


class Resources:
    @staticmethod
    def get(resource_field, resource_type=None, get_by_name=False):
        if not get_by_name or not resource_type:
            attribute = "get_by_id"
        else:
            attribute = "get_by_name"

        if resource_type == ResourceType.UNKNOWN:
            raise ResourceTypeException()

        elif resource_type == ResourceType.IPv4:
            return getattr(IPs, attribute)(resource_field)

        elif resource_type == ResourceType.DOMAIN:
            return getattr(Domains, attribute)(resource_field)

        elif resource_type == ResourceType.EMAIL:
            return getattr(Emails, attribute)(resource_field)

        elif resource_type == ResourceType.HASH:
            return getattr(Hashes, attribute)(resource_field)

        elif resource_type == ResourceType.URL:
            return getattr(URLs, attribute)(resource_field)

        elif resource_type == ResourceType.USERNAME:
            return getattr(Usernames, attribute)(resource_field)

    @staticmethod
    def get_data_from_resources(resource_refs):
        result = []
        if not resource_refs:
            return result

        for resource_ref in resource_refs:
            resource = Resources.get(
                resource_ref["resource_id"],
                ResourceType.get_type_from_string(resource_ref["resource_type"]),
            )

            result.append(resource.get_data())

        return result
