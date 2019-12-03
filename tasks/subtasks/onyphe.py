import traceback
import json
import urllib.request

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("onyphe")


def onyphe_threatlist(ip):
    try:
        URL = f"https://www.onyphe.io/api/threatlist/{ip}?apikey={API_KEY}"
        response = urllib.request.urlopen(URL).read()
        response = json.loads(response)

        threatlists = {"threatlists": []}
        if "results" in response:
            for entry in response["results"]:
                if "threatlist" in entry:
                    threatlists["threatlists"].append(entry["threatlist"])
        threatlists["threatlists"] = list(set(threatlists["threatlists"]))
        threatlists["threatlists"].sort()
        print(threatlists)
        return threatlists

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def onyphe_synscan(ip):
    try:
        URL = f"https://www.onyphe.io/api/synscan/{ip}?apikey={API_KEY}"
        response = urllib.request.urlopen(URL).read()
        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
