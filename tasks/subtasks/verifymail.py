import traceback
import json
import requests

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("verify-email")
URL = "https://app.verify-email.org/api/v1/{key}/verify/{email}"

def verifymail(email):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        vmail = requests.get(URL.format(**{"key": API_KEY, "email": email}), headers=headers)
        if not vmail.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(vmail.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
