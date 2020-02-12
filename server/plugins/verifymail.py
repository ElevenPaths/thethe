import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_result_types import PluginResultStatus

URL = "https://app.verify-email.org/api/v1/{key}/verify/{email}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.EMAIL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = (
    "Connects to the mail server and checks whether the mailbox exists or not"
)
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "verifymail"
PLUGIN_NEEDS_API_KEY = True

API_KEY = KeyRing().get("verify-email")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://verify-email.org/faq.html"
API_KEY_NAMES = ["verify-email"]


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
            verifymail.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def verifymail(plugin_name, project_id, resource_id, resource_type, email):
    response = {}
    result_status = PluginResultStatus.STARTED

    try:
        API_KEY = KeyRing().get("verify-email")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        else:
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            vmail = requests.get(
                URL.format(**{"key": API_KEY, "email": email}), headers=headers
            )
            if not vmail.status_code == 200:
                print("[verifymail]: error!")
                result_status = PluginResultStatus.FAILED
            else:
                response = json.loads(vmail.content)
                if response:
                    result_status = PluginResultStatus.COMPLETED
                else:
                    result_status = PluginResultStatus.RETURN_NONE

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, response, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
