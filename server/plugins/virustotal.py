import traceback
import json
import requests

from tasks.api_keys import KeyRing
from tasks.tasks import celery_app
from server.entities.resource import Resources, ResourceType
from server.plugins.plugin_base import finishing_task

API_KEY = KeyRing().get("virustotal")

url_for_hashes = "https://www.virustotal.com/vtapi/v2/file/report"
url_for_urls = "https://www.virustotal.com/vtapi/v2/url/report"
url_for_domains = "https://www.virustotal.com/vtapi/v2/domain/report"
url_for_ips = "https://www.virustotal.com/vtapi/v2/ip-address/report"


# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.URL,
    ResourceType.HASH,
]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Search a hash or a URL in VirusTotal"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "virustotal"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://developers.virustotal.com/reference"
    autostart = PLUGIN_AUTOSTART
    apikey_in_ddbb = bool(API_KEY)

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        target = self.resource.get_data()["canonical_name"]

        # Canonical data of hashes is its short form so we have to get long hash instead
        if resource_type == ResourceType.HASH:
            target = self.resource.get_data()["hash"]

        try:
            to_task = {
                "target": target,
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }

            virustotal.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def virustotal(plugin_name, project_id, resource_id, resource_type, target):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

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
            print("[VT] Unknown resource type before querying service")
            return None

        response = requests.get(url, params=params)

        if not response.status_code == 200:
            print(response)
            return None
        else:
            response = json.loads(response.content)

        print(response)
        finishing_task(plugin_name, project_id, resource_id, resource_type, response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
