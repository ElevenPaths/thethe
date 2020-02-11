import traceback
import json
import requests

from tasks.api_keys import KeyRing
from tasks.tasks import celery_app
from server.entities.resource_types import ResourceType
from server.entities.plugin_result_types import PluginResultStatus
from server.entities.resource_base import Resource


url_for_hashes = "https://www.virustotal.com/vtapi/v2/file/report"
url_for_urls = "https://www.virustotal.com/vtapi/v2/url/report"
url_for_domains = "https://www.virustotal.com/vtapi/v2/domain/report"
url_for_ips = "https://www.virustotal.com/vtapi/v2/ip-address/report"


# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.DOMAIN,
]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Search a domain in VirusTotal"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "vt_domain"
PLUGIN_NEEDS_API_KEY = True

API_KEY = KeyRing().get("virustotal")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://developers.virustotal.com/reference"
API_KEY_NAMES = ["virustotal"]


class Plugin:
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
                "plugin_name": PLUGIN_NAME,
            }

            vt_domain.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def vt_domain(plugin_name, project_id, resource_id, resource_type, target):
    result_status = PluginResultStatus.STARTED
    response = None

    try:
        API_KEY = KeyRing().get("virustotal")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        else:
            response = None
            url = None
            params = {"apikey": API_KEY}

            resource_type_for_vt = ResourceType(resource_type)

            if resource_type_for_vt == ResourceType.DOMAIN:
                url = url_for_domains
                params["domain"] = target
            elif resource_type_for_vt == ResourceType.URL:
                url = url_for_urls
                params["resource"] = target
            elif resource_type_for_vt == ResourceType.IPv4:
                url = url_for_ips
                params["ip"] = target
            elif resource_type_for_vt == ResourceType.HASH:
                url = url_for_hashes
                params["resource"] = target
            else:
                print("[VT]: Unknown resource type before querying service")
                result_status = PluginResultStatus.FAILED

            response = requests.get(url, params=params)

            if not response.status_code == 200:
                print(response)
                result_status = PluginResultStatus.RETURN_NONE
            else:
                response = json.loads(response.content)
                result_status = PluginResultStatus.COMPLETED

        print(response)

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, response, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
