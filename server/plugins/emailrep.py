import traceback
import json
import requests

from tasks.api_keys import KeyRing
from tasks.tasks import celery_app
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from server.entities.plugin_result_types import PluginResultStatus


# At this time there is no need for an APIKEY
URL = "https://emailrep.io/{email}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.EMAIL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = 'Illuminate the "reputation" behind an email address'
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "emailrep"
PLUGIN_NEEDS_API_KEY = False

API_KEY = KeyRing().get("emailrep")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://emailrep.io/key"
API_KEY_NAMES = ["emailrep"]


class Plugin:
    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "email": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": PLUGIN_NAME,
            }
            emailrep.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def emailrep(plugin_name, project_id, resource_id, resource_type, email):
    try:
        # API Key is not needed bynow 20-01-2020
        # if not API_KEY:
        #     print("No API key...!")
        #     return None

        response = {}
        result_status = PluginResultStatus.STARTED

        headers = {"Accept": "application/json"}
        emailrep_response = requests.get(
            URL.format(**{"email": email}), json={}, headers=headers
        )
        if not emailrep_response.status_code == 200:
            print("Emailrep error!")
            result_status = PluginResultStatus.RETURN_NONE

        else:
            response = json.loads(emailrep_response.content)
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
