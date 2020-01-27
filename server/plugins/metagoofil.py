import os
import traceback
from urllib.parse import urlparse

import tasks.deps.metagoofil.metagoofil as _metagoofil

from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app
from server.plugins.plugin_base import finishing_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.DOMAIN]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = (
    "Information gathering tool for extracting metadata of public documents"
)
PLUGIN_API_KEY = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "metagoofil"
PLUGIN_AUTOSTART = False
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
            to_task = {
                "domain": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            metagoofil.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def metagoofil(domain, plugin_name, project_id, resource_id, resource_type):
    try:
        print("Analizing {} with metagoofil".format(domain))

        response = _metagoofil._main(domain)

        files = []
        for x in response:
            url = urlparse(x)
            filename = os.path.basename(url.path)
            extension = filename.split(".")[1]
            files.append(
                {"filename": filename, "extension": extension.lower(), "url": x}
            )

        finishing_task(plugin_name, project_id, resource_id, resource_type, files)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
