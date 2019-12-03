import traceback
import json
import requests

from tasks.api_keys import KeyRing

# At this time there is no need for an APIKEY
# API_KEY = KeyRing().get("emailrep")
URL = "https://emailrep.io/{email}"


def emailrep(email):
    try:
        # API Key no es necesaria!
        # if not API_KEY:
        #     print("No API key...!")
        #     return None

        response = {}
        headers = {"Accept": "application/json"}
        emailrep_response = requests.get(
            URL.format(**{"email": email}), json={}, headers=headers
        )
        if not emailrep_response.status_code == 200:
            # print("API key error!")
            print("Emailrep error!")
            return None
        else:
            response = json.loads(emailrep_response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
