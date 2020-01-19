import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app

# 250 requests left, 31 days until renewal.
API_KEY = KeyRing().get("binaryedge")
# https://docs.binaryedge.io/api-v2/
URL = "https://api.binaryedge.io/v2/query/ip/{ip}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "List of recent events for the specified host, including details of exposed ports and services"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "binaryedge"
PLUGIN_AUTOSTART = False
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
                "ip": self.resource.get_data()["address"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            binaryedge_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def binaryedge(ip):
    try:

        if not API_KEY:
            print("No API key...!")
            return {}

        response = {}
        headers = {"X-Key": API_KEY}
        response = requests.get(URL.format(**{"ip": ip}), headers=headers)

        if response.status_code == 404:
            print("associated records not found!")
        elif not response.status_code == 200:
            print("API key error!")
        else:
            response = json.loads(response.content)
            print(response)
            return response

        return {}

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None

@celery_app.task
def binaryedge_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = {}
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = binaryedge(ip)
        else:
            print("threatminer resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


