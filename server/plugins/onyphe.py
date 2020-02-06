import json
import traceback
import json
import urllib.request

from tasks.api_keys import KeyRing
from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app
from server.plugins.plugin_base import finishing_task

API_KEY = KeyRing().get("onyphe")

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Lookup onyphe.io wether this IP is included in threatlists"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "onyphe"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://www.onyphe.io/documentation/api"
    autostart = PLUGIN_AUTOSTART
    apikey_in_ddbb = bool(API_KEY)

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
            onyphe.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def onyphe_threatlist(ip):
    try:
        API_KEY = KeyRing().get("onyphe")
        if not API_KEY:
            print("No API key...!")
            return None

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
    try:
        API_KEY = KeyRing().get("onyphe")
        if not API_KEY:
            print("No API key...!")
            return None

        URL = f"https://www.onyphe.io/api/synscan/{ip}?apikey={API_KEY}"
        response = urllib.request.urlopen(URL).read()
        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


@celery_app.task
def onyphe(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = onyphe_threatlist(ip)
        if not query_result:
            return
        print(query_result)

        finishing_task(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
