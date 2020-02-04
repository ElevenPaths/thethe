import traceback
import json
import requests

from tasks.api_keys import KeyRing
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_base import finishing_task


API_KEY = KeyRing().get("hunterio")
URL_DOMAIN = "https://api.hunter.io/v2/domain-search?domain={domain}&api_key={key}"
URL_EMAIL_VERIFIER = (
    "https://api.hunter.io/v2/email-verifier?email={email}&api_key={key}"
)

# URL_EMAIL_FINDER = "https://api.hunter.io/v2/email-finder?domain={domain}&first_name={name}&last_name={lastname}&api_key={key}"

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.DOMAIN, ResourceType.EMAIL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Lists all the people working in a company with their name and email address found on the web"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "hunterio"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://hunter.io/api"
    autostart = PLUGIN_AUTOSTART
    apikey_in_ddbb = bool(API_KEY)

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "target": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            hunterio.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def send_request(url):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        hunterio_response = requests.get(url, headers=headers)
        if not hunterio_response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(hunterio_response.content)

        return response["data"]

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def hunterio_domain(domain):
    url = URL_DOMAIN.format(**{"domain": domain, "key": API_KEY})
    return send_request(url)


def hunterio_email(email):
    url = URL_EMAIL_VERIFIER.format(**{"email": email, "key": API_KEY})
    return send_request(url)


@celery_app.task
def hunterio(plugin_name, project_id, resource_id, resource_type, target):
    try:
        query_result = None

        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = hunterio_domain(target)
        elif resource_type == ResourceType.EMAIL:
            query_result = hunterio_email(target)
        else:
            print("Hunter.io resource type does not found")

        finishing_task(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
