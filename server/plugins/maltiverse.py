# FIXME: This plugins does not work when resource is not a domain
import traceback
import json
import hashlib
import requests

from tasks.deps.maltiverse import Maltiverse
from tasks.api_keys import KeyRing
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_result_types import PluginResultStatus


URL_IP = "https://api.maltiverse.com/ip/{ip}"
URL_DOMAIN = "https://api.maltiverse.com/hostname/{hostname}"
URL_URL = "https://api.maltiverse.com/url/{url}"
URL_HASH = "https://api.maltiverse.com/sample/{hash}"


# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.IPv4,
    ResourceType.DOMAIN,
    ResourceType.URL,
    ResourceType.HASH,
]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Search indicators of compromise or something related"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "maltiverse"
PLUGIN_NEEDS_API_KEY = True

MALTIVERSE_EMAIL = KeyRing().get("maltiverse_email")
MALTIVERSE_PASS = KeyRing().get("maltiverse_pass")
API_KEY_IN_DDBB = bool(MALTIVERSE_EMAIL) & bool(MALTIVERSE_PASS)
API_KEY_DOC = "https://app.swaggerhub.com/apis-docs/maltiverse/api/1.0.0-oas3"
API_KEY_NAMES = ["maltiverse_email", "maltiverse_pass"]

api = Maltiverse()
api.login(MALTIVERSE_EMAIL, password=MALTIVERSE_PASS)


class Plugin:
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
                "plugin_name": PLUGIN_NAME,
            }
            maltiverse.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


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


@celery_app.task
def maltiverse(plugin_name, project_id, resource_id, resource_type, target):
    try:
        MALTIVERSE_EMAIL = KeyRing().get("maltiverse_email")
        MALTIVERSE_PASS = KeyRing().get("maltiverse_pass")
        API_KEY = bool(MALTIVERSE_EMAIL) & bool(MALTIVERSE_PASS)
        query_result = None

        if not API_KEY:
            print(["[maltiverse]: No API Keys..."])
            result_status = PluginResultStatus.NO_API_KEY

        else:

            result_status = PluginResultStatus.STARTED

            resource_type = ResourceType(resource_type)
            if resource_type == ResourceType.IPv4:
                query_result = maltiverse_ip(target)
            elif resource_type == ResourceType.DOMAIN:
                query_result = maltiverse_domain(target)
            elif resource_type == ResourceType.URL:
                query_result = maltiverse_url(target)
            elif resource_type == ResourceType.HASH:
                query_result = maltiverse_hash(target)
            else:
                print("Maltiverse resource type does not found")
                result_status = PluginResultStatus.RETURN_NONE

            if not query_result:
                result_status = PluginResultStatus.RETURN_NONE
            else:
                result_status = PluginResultStatus.COMPLETED

            print(query_result)

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, query_result, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
