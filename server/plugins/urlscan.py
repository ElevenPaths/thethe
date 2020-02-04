import traceback
import json
import time
import requests

from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from tasks.api_keys import KeyRing
from server.plugins.plugin_base import finishing_task

API_KEY = KeyRing().get("urlscan")
SUBMISSION_URL = "https://urlscan.io/api/v1/scan/"
RESULT_URL = "https://urlscan.io/api/v1/result/{uuid}/"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.URL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Scan and analyse URLs"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "urlscan"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://urlscan.io/about-api/"
    autostart = PLUGIN_AUTOSTART
    apikey_in_ddbb = bool(API_KEY)

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "url": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            urlscan.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def result(uuid):
    url_result_response = requests.get(RESULT_URL.format(**{"uuid": uuid}))
    if not url_result_response.status_code == 200:
        print("URL Result API error for uuid {}".format(uuid))
        return None
    return json.loads(url_result_response.content)


@celery_app.task
def urlscan(plugin_name, project_id, resource_id, resource_type, url):

    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
            "Content-Type": "application/json",
            "API-Key": API_KEY,
        }
        data = {"url": url, "public": "on", "tags": ["phishing", "malicious"]}
        url_submission_response = requests.post(
            SUBMISSION_URL, headers=headers, json=data
        )
        if not url_submission_response.status_code == 200:
            print("API key error!")
            return None
        else:
            uuid = json.loads(url_submission_response.content)["uuid"]

            SLEEP_LIMIT = 300
            SLEEP_DELTA_INCREMENT = 2.5
            SLEEP_FRAME = 2
            # Número de reintentos cada 2 segundos
            while SLEEP_FRAME < SLEEP_LIMIT:
                response = result(uuid)
                if response is not None:
                    break
                SLEEP_FRAME = round(SLEEP_FRAME * SLEEP_DELTA_INCREMENT)
                time.sleep(SLEEP_FRAME)

        finishing_task(plugin_name, project_id, resource_id, resource_type, response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
