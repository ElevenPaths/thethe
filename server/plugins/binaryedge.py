# TODO: Unfinished plugin need refactoring

import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_base import finishing_task

# https://docs.binaryedge.io/api-v2/
URL = "https://api.binaryedge.io/v2/query/ip/{ip}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "List of recent events for the specified host, including details of exposed ports and services"
PLUGIN_DISABLE = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "binaryedge"
PLUGIN_NEEDS_API_KEY = True

# 250 requests left, 31 days until renewal.
API_KEY = KeyRing().get("binaryedge")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://docs.binaryedge.io/api-v2/"
API_KEY_NAMES = ["binaryedge"]


class Plugin:
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
            binaryedge.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def binaryedge(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        API_KEY = KeyRing().get("binaryedge")
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

        finishing_task(plugin_name, project_id, resource_id, resource_type, response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
