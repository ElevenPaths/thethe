import dns.resolver as resolver
import traceback

from urllib.parse import urlparse
from server.entities.resource import Resources, ResourceType

from tasks.tasks import celery_app

# If you want to expand DNS query types this is the right place
LOOKUP = ["NS", "A", "AAAA", "MX", "TXT", "SRV"]


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

