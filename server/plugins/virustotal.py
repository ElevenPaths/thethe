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
    ResourceType.URL,
    ResourceType.HASH,
]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Search a hash or a URL in VirusTotal"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "virustotal"
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

            virustotal_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

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

