import traceback
import json
import requests
import re

from urllib.parse import urlparse

from tasks.api_keys import KeyRing
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.entities.plugin_result_types import PluginResultStatus
from server.entities.resource_base import Resource


URL = "https://checkurl.phishtank.com/checkurl/"
SCREENSHOTS_STORAGE_PATH = "/temp/phishtank"
SCREENSHOTS_SERVER_PATH = "static/phishtank"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"


# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.URL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Check in PhishTank if this URL is marked as a phishing"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "phishtank"
PLUGIN_NEEDS_API_KEY = True

API_KEY = KeyRing().get("phishtank")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://www.phishtank.com/api_info.php"
API_KEY_NAMES = ["phishtank"]


class Plugin:
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
                "plugin_name": PLUGIN_NAME,
            }
            phishtank.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


def phishtank_check(url):
    try:
        API_KEY = KeyRing().get("phishtank")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        response = {}

        headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        post_data = {"url": url, "format": "json", "app_key": API_KEY}

        response = requests.post(URL, post_data, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)
            if "phish_id" in response["results"]:
                phish_id = response["results"]["phish_id"]

                try:
                    screenshot_path = phishtank_screenshot(phish_id)
                    if screenshot_path:
                        response["results"]["screenshot_path"] = screenshot_path
                except:
                    print("[PHISHTANK] Could not have a screenshot")

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def phishtank_screenshot(phish_id):
    try:

        URL_main = f"https://www.phishtank.com/phish_screenshot.php?phish_id={phish_id}"

        regex_url = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

        API_KEY = KeyRing().get("phishtank")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        response = {}

        headers = {"User-Agent": USER_AGENT}

        response = requests.get(URL_main, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            if response.content:
                content = response.content.decode("utf-8")
                matches = re.findall(regex_url, content)
                if matches:
                    screenshot_url = matches[0]
                    screenshot_name = urlparse(screenshot_url).path
                    r = requests.get(screenshot_url, allow_redirects=True)
                    with open(
                        f"{SCREENSHOTS_STORAGE_PATH}{screenshot_name}", "wb"
                    ) as f:
                        f.write(r.content)
                    return f"{SCREENSHOTS_SERVER_PATH}{screenshot_name}"

        return None

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def phishtank_tech_details(phish_id):
    try:
        URL_main = f"https://www.phishtank.com/phish_detail.php?phish_id={phish_id}"

        API_KEY = KeyRing().get("phishtank")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        response = {}

        headers = {"User-Agent": USER_AGENT}

        response = requests.get(URL_main, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = response.content

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None  # parsing html to extract Verify and more


@celery_app.task
def phishtank(plugin_name, project_id, resource_id, resource_type, url):
    result_status = PluginResultStatus.STARTED
    query_result = None

    try:
        API_KEY = KeyRing().get("phishtank")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY

        else:
            resource_type = ResourceType(resource_type)
            if resource_type == ResourceType.URL:
                query_result = phishtank_check(url)
                result_status = PluginResultStatus.COMPLETED

            else:
                print("phishtank resource type does not found")
                result_status = PluginResultStatus.RETURN_NONE

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, response, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
