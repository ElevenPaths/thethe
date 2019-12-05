import traceback
import json
import requests

URL_IP = "https://www.threatcrowd.org/searchApi/v2/ip/report/?ip={ip}"
URL_DOMAIN = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
URL_EMAIL = "https://www.threatcrowd.org/searchApi/v2/email/report/?email={email}"
URL_HASH = "https://www.threatcrowd.org/searchApi/v2/file/report/?resource={hash}"


def send_request(url):
    try:
        response = {}
        threatcrowd_response = requests.get(url)
        if not threatcrowd_response.status_code == 200:
            print("Response error!")
            return None
        else:
            response = json.loads(threatcrowd_response.content)
            print(response)
        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def threatcrowd_ip(ip):
    url = URL_IP.format(**{"ip": ip})
    send_request(url)


def threatcrowd_domain(domain):
    url = URL_DOMAIN.format(**{"domain": domain})
    send_request(url)


def threatcrowd_email(email):
    url = URL_EMAIL.format(**{"email": email})
    send_request(url)


def threatcrowd_hash(hash):
    url = URL_HASH.format(**{"hash": hash})
    send_request(url)
