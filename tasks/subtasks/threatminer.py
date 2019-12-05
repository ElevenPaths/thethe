import traceback
import json
import requests

# from tasks.api_keys import KeyRing

# API_KEY = KeyRing().get("binaryedge")

# IMPORTANT NOTE: Please note that the rate limit is set to 10 queries per minute.
API_KEY = ""


def threatminer_searchAPTNotes(fulltext):
    try:
        URL = "https://api.threatminer.org/v2/reports.php?q={fulltext}&rt=1"
        response = {}
        response = requests.get(URL.format(**{"fulltext": fulltext}))
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


def threatminer_APTNotesToIoCs(filename_param, year):
    try:
        URL = (
            "https://api.threatminer.org/v2/report.php?q={filename_param}&y={year}&rt=1"
        )
        response = {}

        response = requests.get(
            URL.format(**{"filename_param": filename_param, "year": year})
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


def threatminer_AVDetection(name_virus):
    try:
        URL = "	https://api.threatminer.org/v2/av.php?q={name_virus}&rt=1"
        response = {}

        response = requests.get(URL.format(**{"name_virus": name_virus}))
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


def threatminer_ip(ip, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/host.php?q={ip}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"ip": ip, "tab_rt": tab_rt}))
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


def threatminer_domain(domain, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/domain.php?q={domain}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"domain": domain, "tab_rt": tab_rt}))
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


def threatminer_samples(hash, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/sample.php?q={hash}}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"hash": hash, "tab_rt": tab_rt}))
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


def threatminer_ssl(hash, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/ssl.php?q={hash}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"hash": hash, "tab_rt": tab_rt}))
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
