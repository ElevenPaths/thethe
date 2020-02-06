import json
import traceback
import json
import urllib.request

from tasks.api_keys import KeyRing
from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app
from server.plugins.plugin_base import finishing_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Use IpStack service to geolocate an IP address"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "geoip"
PLUGIN_AUTOSTART = True
PLUGIN_DISABLE = False

API_KEY = KeyRing().get("geoip")


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://ipstack.com/signup/free"
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
            geoip.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def geoip(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        API_KEY = KeyRing().get("geoip")
        if not API_KEY:
            print("No API key...!")
            return None

        URL = f"http://api.ipstack.com/{ip}?access_key={API_KEY}&format=1"
        response = urllib.request.urlopen(URL).read()
        result = json.loads(response)
        finishing_task(plugin_name, project_id, resource_id, resource_type, result)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
