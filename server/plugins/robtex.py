import traceback
import json
import requests

from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_base import finishing_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Search for an IP number and get which hostnames points to it"
PLUGIN_API_KEY = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "robtex"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False

URL = "https://freeapi.robtex.com/ipquery/{ip}"

API_KEY = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = ""
    autostart = PLUGIN_AUTOSTART
    apikey_in_ddbb = bool(API_KEY)

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
                "plugin_name": Plugin.name,
            }
            robtex.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def robtex(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        response = {}
        robtex_response = requests.get(URL.format(**{"ip": ip}))
        if not robtex_response.status_code == 200:
            print("Robtext error!")
            response = None
        else:
            response = json.loads(robtex_response.content)

        finishing_task(plugin_name, project_id, resource_id, resource_type, response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
