import traceback
import json
import requests

URL = "https://freeapi.robtex.com/ipquery/{ip}"


def robtex(ip):
    try:
        response = {}
        robtex_response = requests.get(URL.format(**{"ip": ip}))
        if not robtex_response.status_code == 200:
            print("Robtext error!")
            response = None
        else:
            response = json.loads(robtex_response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
