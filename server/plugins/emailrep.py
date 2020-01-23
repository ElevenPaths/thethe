import traceback
import json
import requests

from tasks.api_keys import KeyRing
from tasks.tasks import celery_app
from server.entities.resource import Resources, ResourceType
from server.plugins.plugin_base import finishing_task

# At this time there is no need for an APIKEY
# API_KEY = KeyRing().get("emailrep")
URL = "https://emailrep.io/{email}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.EMAIL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = 'Illuminate the "reputation" behind an email address'
PLUGIN_API_KEY = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "emailrep"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = ""
    autostart = PLUGIN_AUTOSTART

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
                "plugin_name": Plugin.name,
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
        headers = {"Accept": "application/json"}
        emailrep_response = requests.get(
            URL.format(**{"email": email}), json={}, headers=headers
        )
        if not emailrep_response.status_code == 200:
            # print("API key error!")
            print("Emailrep error!")
            return None
        else:
            response = json.loads(emailrep_response.content)

        finishing_task(plugin_name, project_id, resource_id, resource_type, response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
