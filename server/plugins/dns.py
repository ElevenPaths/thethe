import json
import traceback
import traceback

from urllib.parse import urlparse

import dns.resolver as resolver

from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.DOMAIN]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Performs a DNS interrogation for a domain"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "dns"
PLUGIN_AUTOSTART = True
PLUGIN_DISABLE = False

# If you want to expand DNS query types this is the right place
LOOKUP = ["NS", "A", "AAAA", "MX", "TXT", "SRV"]

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
            if resource_type == ResourceType.DOMAIN:
                to_task = {
                    "domain": self.resource.get_data()["domain"],
                    "resource_id": self.resource.get_id_as_string(),
                    "project_id": self.project_id,
                    "resource_type": resource_type.value,
                    "plugin_name": Plugin.name,
                }
                dns_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))



def dns(domain):
    try:
        results = {}

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

                except:
                    results[TYPE] = None

        print(results)
        return results

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))

@celery_app.task
def dns_task(plugin_name, project_id, resource_id, resource_type, domain):

    query_result = {}

    # PTR
    try:
        dns_results = dns(domain)
        query_result = dns_results

        # TODO: Probably, we can save some parameters here when object is instantiated
        resource_type = ResourceType(resource_type)

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
