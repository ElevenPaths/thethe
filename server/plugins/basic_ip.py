import whois
import ipwhois
import json
import traceback

from ipwhois import IPWhois
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from dns import resolver, reversename
from server.entities.plugin_base import finishing_task


# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Run a subset of plugins to gather ASN, Network and rDNS information on a IP address"
PLUGIN_API_KEY = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "basic"
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
            if resource_type == ResourceType.IPv4:
                to_task = {
                    "ip": self.resource.get_data()["address"],
                    "resource_id": self.resource.get_id_as_string(),
                    "project_id": self.project_id,
                    "resource_type": resource_type.value,
                    "plugin_name": Plugin.name,
                }
                return basic_ip.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def asn(ip):
    try:
        results = {}
        target = IPWhois(ip)
        lookup = target.lookup_rdap(depth=1)
        if lookup:
            results["asn"] = {
                "asn": lookup["asn"],
                "asn_cidr": lookup["asn_cidr"],
                "asn_country_code": lookup["asn_country_code"],
                "asn_date": lookup["asn_date"],
                "asn_description": lookup["asn_description"],
                "asn_registry": lookup["asn_registry"],
            }

            results["network"] = {
                "cidr": lookup["network"]["cidr"],
                "country": lookup["network"]["country"],
                "handle": lookup["network"]["handle"],
                "name": lookup["network"]["name"],
            }

        return results

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


def ptr(ip):
    try:
        PTR_record = None
        addr = reversename.from_address(ip)
        PTR_record = str(resolver.query(addr, "PTR")[0])
        return PTR_record
    except Exception as e:
        print(e)
        return None


@celery_app.task
def basic_ip(ip, plugin_name, project_id, resource_id, resource_type):

    query_result = {}

    # PTR
    try:
        PTR_record = ptr(ip)

        if PTR_record:
            query_result["ptr"] = PTR_record

        ASN_NET_record = asn(ip)

        if "asn" in ASN_NET_record:
            query_result["asn"] = ASN_NET_record["asn"]

        if "network" in ASN_NET_record:
            query_result["network"] = ASN_NET_record["network"]

        finishing_task(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
