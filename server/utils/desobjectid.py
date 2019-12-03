import traceback
import json

from bson import ObjectId
from collections.abc import Iterable


def desobjectid_cursor(items):
    try:
        result = []
        for item in items:
            for id_keys in item.keys():
                if id_keys.endswith("_id"):
                    item[id_keys] = str(item[id_keys])
            result.append(item)
        return result
    except TypeError as e:
        return str(items)
    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
