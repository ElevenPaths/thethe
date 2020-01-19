import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app

API_KEY = KeyRing().get("verify-email")
URL = "https://app.verify-email.org/api/v1/{key}/verify/{email}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.EMAIL]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Connects to the mail server and checks whether the mailbox exists or not"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "verifymail"
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

        try:
            to_task = {
                "email": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            verifymail_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def verifymail(email):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        vmail = requests.get(URL.format(**{"key": API_KEY, "email": email}), headers=headers)
        if not vmail.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(vmail.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None

@celery_app.task
def verifymail_task(plugin_name, project_id, resource_id, resource_type, email):
    try:
        query_result = verifymail(email)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))

