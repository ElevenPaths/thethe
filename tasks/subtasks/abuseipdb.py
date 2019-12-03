import traceback
import json
import requests

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("abuseipdb")
URL = "https://api.abuseipdb.com/api/v2/check"


def abuseipdb(ip):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        headers = {"Accept": "application/json", "Key": API_KEY}
        data = {"ipAddress": ip}
        abuse_response = requests.get(URL, headers=headers, json=data)
        if not abuse_response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(abuse_response.content)
            print(response)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
