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

from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app

# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.DOMAIN,
]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Search a domain in VirusTotal"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "vt_domain"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


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

        target = self.resource.get_data()["canonical_name"]


        try:
            to_task = {
                "target": target,
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }

            virustotal_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


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



@celery_app.task
def virustotal_task(plugin_name, project_id, resource_id, resource_type, target):
    try:
        query_result = None

        resource_type = ResourceType(resource_type)
        query_result = virustotal(target, resource_type)

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
