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


from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app


# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.IPv4,
    ResourceType.DOMAIN,
    ResourceType.URL,
    ResourceType.HASH,
]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "OTX AlienVault Feeds Threats"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "otx"
PLUGIN_AUTOSTART = False
# TODO: Plugin need testing before enabling it
PLUGIN_DISABLE = True


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    autostart = PLUGIN_AUTOSTART

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "target": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            otx_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


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


@celery_app.task
def otx_task(plugin_name, project_id, resource_id, resource_type, target):
    try:
        resource_type = ResourceType(resource_type)
        # Check 2nd parameter if it's sent through view (frontend)
        if resource_type == ResourceType.IPv4:
            query_result = otx_iocs_ipv4(target, "general")
        elif resource_type == ResourceType.DOMAIN:
            query_result = otx_iocs_hostname(target, "general")
        elif resource_type == ResourceType.URL:
            query_result = otx_iocs_url(target, "general")
        elif resource_type == ResourceType.HASH:
            query_result = otx_iocs_file(target, "analysis")
        else:
            print("OTX resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
