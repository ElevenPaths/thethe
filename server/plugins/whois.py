import whois as whois_pkg

# import ipwhois
import json
import traceback

from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_result_types import PluginResultStatus
from server.entities.resource_base import Resource

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.DOMAIN, ResourceType.EMAIL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = True
PLUGIN_DESCRIPTION = "Performs a WHOIS request for a domain"
PLUGIN_DISABLE = False
PLUGIN_NAME = "whois"
PLUGIN_IS_ACTIVE = False
PLUGIN_NEEDS_API_KEY = False

API_KEY = False
API_KEY_IN_DDBB = False
API_KEY_DOC = None
API_KEY_NAMES = []


class Plugin:
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
                    "plugin_name": PLUGIN_NAME,
                }

                whois.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def whois(plugin_name, project_id, resource_id, resource_type, domain):
    response = None
    result_status = PluginResultStatus.STARTED

    try:
        query_result = whois_pkg.whois(domain)
        if query_result:
            result_status = PluginResultStatus.COMPLETED
        else:
            result_status = PluginResultStatus.RETURN_NONE

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, response, result_status
            )

    except whois.parser.PywhoisError:
        print(f"Domain {domain} does not exists")
        result_status = PluginResultStatus.RETURN_NONE
        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, response, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
