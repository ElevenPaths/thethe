import validators
import re

from enum import Enum


class HashType(Enum):
    UNKNOWN = 0
    MD5 = "MD5"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA512 = "SHA512"

    @staticmethod
    def hash_detection(resource):
        md5_regex = r"^[A-Fa-f0-9]{32}$"
        sha1_regex = r"^[A-Fa-f0-9]{40}$"
        sha256_regex = r"^[A-Fa-f0-9]{64}$"
        sha512_regex = r"^[A-Fa-f0-9]{128}$"

        if re.fullmatch(md5_regex, resource):
            return HashType.MD5
        elif re.fullmatch(sha1_regex, resource):
            return HashType.SHA1
        elif re.fullmatch(sha256_regex, resource):
            return HashType.SHA256
        elif re.fullmatch(sha512_regex, resource):
            return HashType.SHA512

        return HashType.UNKNOWN
