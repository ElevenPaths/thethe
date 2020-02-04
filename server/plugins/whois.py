import whois as whois_pkg

# import ipwhois
import json
import traceback

from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_base import finishing_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.DOMAIN, ResourceType.EMAIL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Performs a WHOIS request for a domain"
PLUGIN_API_KEY = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "whois"
PLUGIN_AUTOSTART = True
PLUGIN_DISABLE = False

API_KEY = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = ""
    autostart = PLUGIN_AUTOSTART
    apikey_in_ddbb = bool(API_KEY)

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            if (
                resource_type == ResourceType.DOMAIN
                or resource_type == ResourceType.EMAIL
            ):
                to_task = {
                    "domain": self.resource.get_data()["domain"],
                    "resource_id": self.resource.get_id_as_string(),
                    "project_id": self.project_id,
                    "resource_type": resource_type.value,
                    "plugin_name": Plugin.name,
                }

                whois.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def whois(plugin_name, project_id, resource_id, resource_type, domain):

    try:
        query_result = whois_pkg.whois(domain)  # json.loads(str(whois.whois(domain)))

        finishing_task(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except whois.parser.PywhoisError:
        print(f"Domain {domain} does not exists")

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
