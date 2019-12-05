# User zigineki@getnada.com
# https://otx.alienvault.com/settings

import traceback
import json
import requests, base64

from tasks.api_keys import KeyRing

# https://otx.alienvault.com/api/v1/indicators/file/6c5360d41bd2b14b1565f5b18e5c203cf512e493/analysis
API_KEY = KeyRing().get("otx")

URL_HASH = "https://otx.alienvault.com/api/v1/indicators/file/{file_hash}/{section}"
URL_URL = "https://otx.alienvault.com/api/v1/indicators/url/{url}/{section}"
URL_HOSTNAME = (
    "https://otx.alienvault.com/api/v1/indicators/hostname/{hostname}/{section}"
)
URL_IPv4 = "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/{section}"
URL_IPv6 = "https://otx.alienvault.com/api/v1/indicators/IPv6/{ip}/{section}"


def otx_iocs_file(file_hash, section):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
            "X-OTX-API-KEY": API_KEY,
        }
        print("testessss ")
        response = requests.get(
            URL_HASH.format(**{"file_hash": file_hash, "section": section}),
            headers=headers,
        )
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


def otx_iocs_url(url, section):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
            "X-OTX-API-KEY": API_KEY,
        }
        response = requests.get(
            URL_URL.format(**{"url": url, "section": section}), headers=headers
        )
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


def otx_iocs_hostname(hostname, section):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
            "X-OTX-API-KEY": API_KEY,
        }
        response = requests.get(
            URL_URL.format(**{"hostname": hostname, "section": section}),
            headers=headers,
        )
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


def otx_iocs_ipv4(ip, section):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
            "X-OTX-API-KEY": API_KEY,
        }
        response = requests.get(
            URL_IPv4.format(**{"ip": ip, "section": section}), headers=headers
        )
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


def otx_iocs_ipv6(ip, section):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
            "X-OTX-API-KEY": API_KEY,
        }
        response = requests.get(
            URL_IPv6.format(**{"ip": ip, "section": section}), headers=headers
        )
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
