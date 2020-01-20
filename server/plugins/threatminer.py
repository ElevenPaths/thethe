# TODO: Untested plugin. Disabled
import json
import traceback

from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app
import json
import requests

# from tasks.api_keys import KeyRing

# API_KEY = KeyRing().get("binaryedge")

# IMPORTANT NOTE: Please note that the rate limit is set to 10 queries per minute.
API_KEY = ""

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.DOMAIN]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "List Threats for domain"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "threatminer"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = True


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
                threatminer_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def threatminer_searchAPTNotes(fulltext):
    try:
        URL = "https://api.threatminer.org/v2/reports.php?q={fulltext}&rt=1"
        response = {}
        response = requests.get(URL.format(**{"fulltext": fulltext}))
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def threatminer_APTNotesToIoCs(filename_param, year):
    try:
        URL = (
            "https://api.threatminer.org/v2/report.php?q={filename_param}&y={year}&rt=1"
        )
        response = {}

        response = requests.get(
            URL.format(**{"filename_param": filename_param, "year": year})
        )
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def threatminer_AVDetection(name_virus):
    try:
        URL = "	https://api.threatminer.org/v2/av.php?q={name_virus}&rt=1"
        response = {}

        response = requests.get(URL.format(**{"name_virus": name_virus}))
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def threatminer_ip(ip, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/host.php?q={ip}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"ip": ip, "tab_rt": tab_rt}))
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def threatminer_domain(domain, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/domain.php?q={domain}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"domain": domain, "tab_rt": tab_rt}))
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def threatminer_samples(hash, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/sample.php?q={hash}}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"hash": hash, "tab_rt": tab_rt}))
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def threatminer_ssl(hash, tab_rt):
    try:
        URL = "https://api.threatminer.org/v2/ssl.php?q={hash}&rt={tab_rt}"
        response = {}

        response = requests.get(URL.format(**{"hash": hash, "tab_rt": tab_rt}))
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


@celery_app.task
def threatminer_task(plugin_name, project_id, resource_id, resource_type, domain):
    try:
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = threatminer_domain(domain, "1")
        else:
            print("threatminer resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
