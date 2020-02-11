import traceback
import json
import requests

from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_result_types import PluginResultStatus


# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Search for an IP number and get which hostnames points to it"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "robtex"
PLUGIN_NEEDS_API_KEY = False

URL = "https://freeapi.robtex.com/ipquery/{ip}"

API_KEY = False
# API_KEY = KeyRing().get("robtex")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = ""
API_KEY_NAMES = []


class Plugin:
    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "ip": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": PLUGIN_NAME,
            }
            robtex.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def robtex(plugin_name, project_id, resource_id, resource_type, ip):
    response = {}
    result_status = PluginResultStatus.STARTED

    try:

        robtex_response = requests.get(URL.format(**{"ip": ip}))
        if not robtex_response.status_code == 200:
            print("Robtext error!")
            result_status = PluginResultStatus.RETURN_NONE
        else:
            response = json.loads(robtex_response.content)
            result_status = PluginResultStatus.COMPLETED

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, response, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
