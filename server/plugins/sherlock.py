import traceback
import os
import json

import tasks.deps.sherlock.sherlock as _sherlock

from server.entities.resource import Resources, ResourceType
from tasks.tasks import celery_app
from server.plugins.plugin_base import finishing_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.USERNAME]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Use Sherlock to find usernames across many social networks"
PLUGIN_API_KEY = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "sherlock"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = ""
    autostart = PLUGIN_AUTOSTART

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "username": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            sherlock.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def sherlock(username, plugin_name, project_id, resource_id, resource_type):
    try:
        site_data_all = None
        data_file_path = os.path.join(
            os.getcwd(), "tasks", "deps", "sherlock", "data.json"
        )

        if site_data_all is None:
            # Check if the file exists otherwise exit.
            if not os.path.exists(data_file_path):
                print("JSON file at doesn't exist.")
                print(
                    "If this is not a file but a website, make sure you have appended http:// or https://."
                )
                return None
            else:
                raw = open(data_file_path, "r", encoding="utf-8")
                try:
                    site_data_all = json.load(raw)
                except:
                    print("Invalid JSON loaded from file.")

        result = _sherlock.sherlock(username, site_data_all, print_found_only=False)

        response = []
        for service in result:
            temp_result = {}
            temp_result["sitename"] = service
            temp_result["exists"] = result.get(service).get("exists")
            temp_result["url_user"] = result.get(service).get("url_user")
            response.append(temp_result)

        finishing_task(plugin_name, project_id, resource_id, resource_type, response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
