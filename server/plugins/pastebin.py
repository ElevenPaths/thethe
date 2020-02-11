import json
import traceback
import pprint
import time
import requests

from server.db import DB
from server.entities.pastebin_manager import PastebinManager, Paste
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from server.entities.plugin_result_types import PluginResultStatus

from tasks.api_keys import KeyRing
from tasks.googlesearch import restricted_googlesearch
from tasks.tasks import celery_app


# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.IPv4,
    ResourceType.DOMAIN,
    ResourceType.EMAIL,
    ResourceType.HASH,
    ResourceType.URL,
    ResourceType.USERNAME,
]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Use Google Search API to retrieve 'pastebin.com' results"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "pastebin"
PLUGIN_NEEDS_API_KEY = True

API_KEY = KeyRing().get("pastebin")
API_KEY_IN_DDBB = bool(API_KEY)
API_KEY_DOC = "https://pastebin.com/doc_scraping_api"
API_KEY_NAMES = ["pastebin"]


# This is the engine for pastebin, other sites should be created in control panel (GMAIL ACCOUNT REQUIRED)
SEARCH_ENGINE = "002161999705497793957:w2bsgwyai92"

# pastebin.com says 1 second between queries, so be cautious and lets it be 1.1 seconds
# https://pastebin.com/doc_scraping_api#5
RATE_LIMIT = 1.1

METADATA_URL = "https://scrape.pastebin.com/api_scrape_item_meta.php?i="
RAWPASTE_URL = "https://scrape.pastebin.com/api_scrape_item.php?i="


class Plugin:
    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        target = self.resource.get_data()["canonical_name"]

        # Canonical data of hashes is its short form so we have to get long hash instead
        if resource_type == ResourceType.HASH:
            target = self.resource.get_data()["hash"]

        try:
            to_task = {
                "target": target,
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": PLUGIN_NAME,
                "search_engine": SEARCH_ENGINE,
            }
            pastebin.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def pastebin(
    plugin_name, project_id, resource_id, resource_type, target, search_engine
):
    try:
        query_result = None
        API_KEY = KeyRing().get("pastebin")
        if not API_KEY:
            print("No API key...!")
            result_status = PluginResultStatus.NO_API_KEY
        else:
            # We use "googlesearch" subtask to gather results as pastebin.com does not
            # have a in-search engine
            query_result = restricted_googlesearch(search_engine, target)

            # Now, process google results and get the pastes and metadata
            if query_result:
                query_result = pastebin_get_results(query_result)
                result_status = PluginResultStatus.COMPLETED
            else:
                result_status = PluginResultStatus.RETURN_NONE

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, query_result, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


def get_key_from_paste_key(item):
    return item.split("/")[-1]


def pastebin_get_results(results):
    try:
        if not API_KEY:
            raise Exception("No API_KEY for pastebin")

        links = []
        if "items" in results:
            links = [item["link"] for item in results["items"]]
        pastebins_refs = []

        for link in links:
            paste_key = get_key_from_paste_key(link)
            try:
                time.sleep(RATE_LIMIT)

                args = {}
                meta = requests.get(METADATA_URL + paste_key)
                if meta.status_code == 200:
                    try:
                        meta = meta.json()[0]
                    except:
                        print(f"This paste {paste_key} has been deleted")
                        continue
                else:
                    print(f"Error {meta.status_code} getting paste from pastebin.com")
                    continue

                for field in [
                    "size",
                    "title",
                    "user",
                    "hits",
                    "date",
                    "syntax",
                    "expire",
                ]:
                    args[field] = meta[field]

                paste = Paste(paste_key, args)

                time.sleep(RATE_LIMIT)

                result = requests.get(RAWPASTE_URL + paste_key)

                if result.status_code == 200:
                    paste.set_content(result.content)

                pastebins_refs.append(paste.save())

            except Exception as e:
                print(f"Failed to get pastebin: {link}")
                tb1 = traceback.TracebackException.from_exception(e)
                print("".join(tb1.format()))
                continue

        if len(pastebins_refs) == 0 or len(links) == 0:
            return None
        return pastebins_refs

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
