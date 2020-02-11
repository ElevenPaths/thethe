import json
import traceback
import json
import urllib.request

from tasks.api_keys import KeyRing
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app


# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Lookup onyphe.io wether this IP is included in threatlists"
PLUGIN_IS_ACTIVE = False
PLUGIN_DISABLE = False
PLUGIN_NAME = "onyphe"
PLUGIN_NEEDS_API_KEY = True

API_KEY = KeyRing().get("onyphe")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://www.onyphe.io/documentation/api"
API_KEY_NAMES = ["onyphe"]


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
                "plugin_name": PLUGIN_NAME,
            }
            onyphe.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def onyphe_threatlist(ip):
    try:
        URL = f"https://www.onyphe.io/api/threatlist/{ip}?apikey={API_KEY}"
        response = urllib.request.urlopen(URL).read()
        response = json.loads(response)

        threatlists = {"threatlists": []}
        if "results" in response:
            for entry in response["results"]:
                if "threatlist" in entry:
                    threatlists["threatlists"].append(entry["threatlist"])
        threatlists["threatlists"] = list(set(threatlists["threatlists"]))
        threatlists["threatlists"].sort()
        return threatlists

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def onyphe_synscan(ip):
    result_status = PluginResultStatus.STARTED
    reponse

    try:
        API_KEY = KeyRing().get("onyphe")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        URL = f"https://www.onyphe.io/api/synscan/{ip}?apikey={API_KEY}"
        response = urllib.request.urlopen(URL).read()
        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


@celery_app.task
def onyphe(plugin_name, project_id, resource_id, resource_type, ip):
    result_status = PluginResultStatus.STARTED
    query_result = None

    try:
        API_KEY = KeyRing().get("onyphe")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        else:
            query_result = onyphe_threatlist(ip)
            if not query_result:
                result_status = PluginResultStatus.RETURN_NONE
            else:
                print(query_result)
                result_status = PluginResultStatus.COMPLETED

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, query_result, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
