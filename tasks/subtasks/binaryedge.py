import traceback
import json
import requests

from tasks.api_keys import KeyRing

# 250 requests left, 31 days until renewal.
API_KEY = KeyRing().get("binaryedge")
# https://docs.binaryedge.io/api-v2/
URL = "https://api.binaryedge.io/v2/query/ip/{ip}"


def binaryedge(ip):
    try:

        if not API_KEY:
            print("No API key...!")
            return {}

        response = {}
        headers = {"X-Key": API_KEY}
        response = requests.get(URL.format(**{"ip": ip}), headers=headers)

        if response.status_code == 404:
            print("associated records not found!")
        elif not response.status_code == 200:
            print("API key error!")
        else:
            response = json.loads(response.content)
            print(response)
            return response

        return {}

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
