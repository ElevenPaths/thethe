import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app
from server.plugins.plugin_base import finishing_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Use Shodan to get information about an IP address"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "shodan"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False

API_KEY = KeyRing().get("shodan")
URL = "https://api.shodan.io/shodan/host/{ip}?key={API_KEY}"


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://developer.shodan.io/api"
    autostart = PLUGIN_AUTOSTART

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
                "plugin_name": Plugin.name,
            }
            shodan.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def shodan(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        ipinfo = requests.get(URL.format(**{"ip": ip, "API_KEY": API_KEY}))
        if not ipinfo.status_code == 200:
            return None
        else:
            ipinfo = json.loads(ipinfo.content)

        response["hostnames"] = ipinfo["hostnames"] if "hostnames" in ipinfo else []
        response["os"] = ipinfo["os"] if "os" in ipinfo else None
        response["org"] = ipinfo["org"] if "org" in ipinfo else None
        response["isp"] = ipinfo["isp"] if "isp" in ipinfo else None
        response["services"] = []

        for data in ipinfo["data"]:
            service = {}
            service["port"] = data["port"] if "port" in data else None
            service["transport"] = data["transport"] if "transport" in data else None
            service["service"] = data["service"] if "service" in data else None
            service["data"] = data["data"] if "data" in data else None
            service["product"] = data["product"] if "product" in data else None
            service["banner"] = data["banner"] if "banner" in data else None
            service["devicetype"] = data["devicetype"] if "devicetype" in data else None
            service["timestamp"] = data["timestamp"] if "timestamp" in data else None
            service["hostnames"] = data["hostnames"] if "hostnames" in data else []

            response["services"].append(service)

        finishing_task(plugin_name, project_id, resource_id, resource_type, response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
