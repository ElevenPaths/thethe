# https://www.hybrid-analysis.com/
# user: zigineki@getnada.com
# pass: Developer1

import traceback
import json
import requests, base64

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("hybrid")
SECRET = KeyRing().get("hybrid_secret")

URL = "https://www.hybrid-analysis.com/api/v2"
PATH_HASH = "/search/hash"
PATH_TERMS = "/search/terms"


def hybrid_search_hash(hash):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {"User-Agent": "Falcon Sandbox", "api-key": API_KEY}
        post_data = {"hash": hash}

        response = requests.post(URL + PATH_HASH, post_data, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


# https://www.hybrid-analysis.com/docs/api/v2#/Search/post_search_terms
# param = host, domain, url
def hybrid_search_terms(param):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {"User-Agent": "Falcon Sandbox", "api-key": API_KEY}

        post_data = {"domain": param}

        response = requests.post(URL + PATH_TERMS, post_data, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
