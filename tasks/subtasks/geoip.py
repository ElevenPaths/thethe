import traceback
import json
import urllib.request

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("ipstack")


def geoip(ip):
    try:
        URL = f"http://api.ipstack.com/{ip}?access_key={API_KEY}&format=1"
        response = urllib.request.urlopen(URL).read()
        return json.loads(response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
