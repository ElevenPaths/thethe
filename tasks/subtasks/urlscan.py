import traceback
import json
import time
import requests

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("urlscan")
SUBMISSION_URL = "https://urlscan.io/api/v1/scan/"
RESULT_URL = "https://urlscan.io/api/v1/result/{uuid}/"


def result(uuid):
    url_result_response = requests.get(RESULT_URL.format(**{"uuid": uuid}))
    if not url_result_response.status_code == 200:
        print("URL Result API error for uuid {}".format(uuid))
        return None
    else:
        return json.loads(url_result_response.content)


def urlscan(url):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
            "Content-Type": "application/json",
            "API-Key": API_KEY,
        }
        data = {"url": url, "public": "on", "tags": ["phishing", "malicious"]}
        url_submission_response = requests.post(
            SUBMISSION_URL, headers=headers, json=data
        )
        if not url_submission_response.status_code == 200:
            print("API key error!")
            return None
        else:
            uuid = json.loads(url_submission_response.content)["uuid"]

            SLEEP_LIMIT = 300
            SLEEP_DELTA_INCREMENT = 2.5
            SLEEP_FRAME = 2
            # Número de reintentos cada 2 segundos
            while SLEEP_FRAME < SLEEP_LIMIT:
                response = result(uuid)
                if response is not None:
                    break
                SLEEP_FRAME = round(SLEEP_FRAME * SLEEP_DELTA_INCREMENT)
                time.sleep(SLEEP_FRAME)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
