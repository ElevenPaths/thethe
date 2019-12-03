import validators
import re
from enum import Enum
from server.entities.hash_types import HashType


class ResourceType(Enum):
    UNKNOWN = None
    URL = "url"
    DOMAIN = "domain"
    EMAIL = "email"
    IPv4 = "ip"
    HASH = "hash"
    FILE = "file"
    USERNAME = "username"

    @classmethod
    def get_type_from_string(cls, resource_as_string):
        try:
            return ResourceType(resource_as_string)
        except ValueError:
            return ResourceType.UNKNOWN

    @classmethod
    def get_values(cls):
        return [cls[t].value for t in cls.__members__.keys()]

    @classmethod
    def validate(cls, resource):
        temp_username = f"{resource}@thethe.com"

        try:
            if validators.ipv4(resource):
                return ResourceType.IPv4

            elif validators.domain(resource):
                return ResourceType.DOMAIN

            elif validators.url(resource):
                return ResourceType.URL

            elif validators.email(resource):
                return ResourceType.EMAIL

            elif (
                HashType.hash_detection(resource) in HashType
                and not HashType.hash_detection(resource) == HashType.UNKNOWN
            ):
                return ResourceType.HASH

            # EYES HERE! We check a username as a contrived email
            # See temp_username
            elif validators.email(temp_username):
                return ResourceType.USERNAME

            print("[!] No resource type has found for your resource: {resource}")
            return ResourceType.UNKNOWN

        except Exception as e:
            raise Exception()

    @classmethod
    def validate_ip_or_domain(cls, resource):
        regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(:[0-9]+)?$"
        if re.match(regex, resource):
            return ResourceType.IPv4
        return ResourceType.DOMAIN


class ResourceTypeException(BaseException):
    pass
