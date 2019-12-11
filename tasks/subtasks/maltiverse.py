import traceback
import json
import hashlib
import requests

from tasks.deps.maltiverse import Maltiverse
from tasks.api_keys import KeyRing


MALTIVERSE_EMAIL = KeyRing().get("maltiverse_email")
MALTIVERSE_PASS = KeyRing().get("maltiverse_pass")

api = Maltiverse()
api.login(MALTIVERSE_EMAIL, password=MALTIVERSE_PASS)

URL_IP = "https://api.maltiverse.com/ip/{ip}"
URL_DOMAIN = "https://api.maltiverse.com/hostname/{hostname}"
URL_URL = "https://api.maltiverse.com/url/{url}"
URL_HASH = "https://api.maltiverse.com/sample/{hash}"


def send_request(url):
    try:
        response = {}
        maltiverse_response = requests.get(url)
        if not maltiverse_response.status_code == 200:
            print("Response error!")
            print(maltiverse_response.content)
            response = None
        else:
            response = json.dumps(json.loads(maltiverse_response.content))

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def maltiverse_ip(ip):
    # url = URL_IP.format(**{"ip": ip})
    # send_request(url)
    return api.ip_get(ip)


def maltiverse_domain(hostname):
    # url = URL_DOMAIN.format(**{"hostname": hostname})
    # send_request(url)
    return api.hostname_get(hostname)


def maltiverse_url(url_original):
    # hash_url = hashlib.sha256(url_original.encode('utf-8')).hexdigest()
    # url = URL_URL.format(**{"url": hash_url})
    # send_request(url)
    return api.url_get(url_original)


def maltiverse_hash(hash):
    # url = URL_HASH.format(**{"hash": hash})
    # send_request(url)
    return api.sample_get(hash)
