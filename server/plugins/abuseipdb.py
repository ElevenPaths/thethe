import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_result_types import PluginResultStatus

URL = "https://api.abuseipdb.com/api/v2/check"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Check the report history of any IP address to see if anyone else has reported malicious activities"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "abuseipdb"
PLUGIN_NEEDS_API_KEY = True

API_KEY = KeyRing().get("abuseipdb")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://www.abuseipdb.com/api"
API_KEY_NAMES = ["abuseipdb"]


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
            abuseipdb.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def abuseipdb(ip, plugin_name, project_id, resource_id, resource_type):
    try:
        result_status = PluginResultStatus.STARTED
        API_KEY = KeyRing().get("abuseipdb")
        response = {}

        if not API_KEY:
            print("[abuseipdb]: No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        else:
            headers = {"Accept": "application/json", "Key": API_KEY}
            data = {"ipAddress": ip}
            abuse_response = requests.get(URL, headers=headers, json=data)

            if not abuse_response.status_code == 200:
                print("[abuseipdb]: Return non 200 code")
                result_status = PluginResultStatus.RETURN_NONE

            else:
                response = json.loads(abuse_response.content)
                print(response)
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
