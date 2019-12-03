import traceback
import json
import requests

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("haveibeenpwned")
URL = "https://haveibeenpwned.com/api/v3/{service}/{account}"


def breach_detail_filler(sites):
    blob = None
    with open("tasks/deps/haveibeenpwned/breaches.json", "r") as f:
        blob = json.loads(f.read())

    if not blob:
        return []

    results = []

    sites = [site["Name"] for site in sites]

    return [entry for entry in blob if entry["Name"] in sites]


def haveibeenpwned(email):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = []
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
            "hibp-api-key": API_KEY,
        }
        hibp = requests.get(
            URL.format(**{"service": "breachedaccount", "account": email}),
            headers=headers,
        )
        if not hibp.status_code == 200:
            print("HIBP Request error!")
            return None
        else:
            hibp = json.loads(hibp.content)
            response = hibp

        details = breach_detail_filler(response)
        if not len(details) == len(response):
            print("[HIBP] An update should be needed in breaches.json file")

        return details

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
