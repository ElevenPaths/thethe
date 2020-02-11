import traceback

from server.entities.resource_types import ResourceType
from server.entities.resource_base import Resource
from tasks.tasks import celery_app
import json
import requests

from tasks.api_keys import KeyRing


URL = "https://haveibeenpwned.com/api/v3/{service}/{account}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.EMAIL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Check if this account has been compromised in a data breach"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "haveibeenpwned"
PLUGIN_NEEDS_API_KEY = True

API_KEY = KeyRing().get("haveibeenpwned")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://haveibeenpwned.com/API/v3"
API_KEY_NAMES = ["haveibeenpwned"]


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
            haveibeenpwned.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def breach_detail_filler(sites):
    blob = None
    with open("tasks/deps/haveibeenpwned/breaches.json", "r") as f:
        blob = json.loads(f.read())

    if not blob:
        return []

    results = []

    sites = [site["Name"] for site in sites]

    return [entry for entry in blob if entry["Name"] in sites]


@celery_app.task
def haveibeenpwned(plugin_name, project_id, resource_id, resource_type, email):
    try:
        API_KEY = KeyRing().get("haveibeenpwned")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        else:
            response = []
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
                "hibp-api-key": API_KEY,
            }
            hibp = requests.get(
                URL.format(**{"service": "breachedaccount", "account": email}),
                headers=headers,
            )

            if not hibp.status_code == 200:
                print("HIBP Request error!")
                result_status = PluginResultStatus.RETURN_NONE

            else:
                hibp = json.loads(hibp.content)
                response = hibp
                result_status = PluginResultStatus.COMPLETED

            details = breach_detail_filler(response)
            if not len(details) == len(response):
                print("[HIBP] An update should be needed in breaches.json file")
                result_status = PluginResultStatus.FAILED

            resource = Resource(resource_id)
            if resource:
                resource.set_plugin_results(
                    plugin_name, project_id, response, result_status
                )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
