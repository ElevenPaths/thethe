import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource_types import ResourceType

API_KEY = KeyRing().get("virustotal")

url_for_hashes = "https://www.virustotal.com/vtapi/v2/file/report"
url_for_urls = "https://www.virustotal.com/vtapi/v2/url/report"
url_for_domains = "https://www.virustotal.com/vtapi/v2/domain/report"
url_for_ips = "https://www.virustotal.com/vtapi/v2/ip-address/report"


def virustotal(resource, resource_type):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = None
        url = None
        params = {"apikey": API_KEY}

        if resource_type == ResourceType.DOMAIN:
            url = url_for_domains
            params["domain"] = resource
        elif resource_type == ResourceType.URL:
            url = url_for_urls
            params["resource"] = resource
        elif resource_type == ResourceType.IPv4:
            url = url_for_ips
            params["ip"] = resource
        elif resource_type == ResourceType.HASH:
            url = url_for_hashes
            params["resource"] = resource
        else:
            print("[VT] Unknown resource type before querying service")
            return None

        response = requests.get(url, params=params)

        if not response.status_code == 200:
            print(response)
            return None
        else:
            response = json.loads(response.content)

        print(response)
        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
