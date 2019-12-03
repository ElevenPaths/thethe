import traceback
import json
import requests

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("hunterio")
URL_DOMAIN = "https://api.hunter.io/v2/domain-search?domain={domain}&api_key={key}"
URL_EMAIL_VERIFIER = (
    "https://api.hunter.io/v2/email-verifier?email={email}&api_key={key}"
)

# URL_EMAIL_FINDER = "https://api.hunter.io/v2/email-finder?domain={domain}&first_name={name}&last_name={lastname}&api_key={key}"


def send_request(url):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        hunterio_response = requests.get(url, headers=headers)
        if not hunterio_response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(hunterio_response.content)

        return response["data"]

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def hunterio_domain(domain):
    url = URL_DOMAIN.format(**{"domain": domain, "key": API_KEY})
    return send_request(url)


def hunterio_email(email):
    url = URL_EMAIL_VERIFIER.format(**{"email": email, "key": API_KEY})
    return send_request(url)
