import json
import traceback
import traceback

from urllib.parse import urlparse

import dns.resolver as resolver

from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_base import finishing_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.DOMAIN]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = True
PLUGIN_DESCRIPTION = "Performs a DNS interrogation for a domain"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "dns"
PLUGIN_NEEDS_API_KEY = False

API_KEY = False
API_KEY_IN_DDBB = False
API_KEY_DOC = ""
API_KEY_NAMES = []

# If you want to expand DNS query types this is the right place
LOOKUP = ["NS", "A", "AAAA", "MX", "TXT", "SRV"]


class Plugin:
    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            if resource_type == ResourceType.DOMAIN:
                to_task = {
                    "domain": self.resource.get_data()["domain"],
                    "resource_id": self.resource.get_id_as_string(),
                    "project_id": self.project_id,
                    "resource_type": resource_type.value,
                    "plugin_name": PLUGIN_NAME,
                }
                dns.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def dns(plugin_name, project_id, resource_id, resource_type, domain):
    try:
        results = {}
        result_status = PluginResultStatus.STARTED

        for TYPE in LOOKUP:
            try:
                r = resolver.query(domain, TYPE)
                results[TYPE] = [str(i) for i in r]

            except:
                # Case when the query must be on canonical domain
                try:
                    root_name = ".".join(domain.split(".")[-2:])
                    r = resolver.query(root_name, TYPE)
                    results[TYPE] = [str(i) for i in r]
                    result_status = PluginResultStatus.COMPLETED

                except:
                    results[TYPE] = None

        if len(LOOKUP) == 0:
            result_status = PluginResultStatus.RETURN_NONE

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(plugin_name, project_id, results, result_status)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
