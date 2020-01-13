import traceback

from server.entities.resource_types import ResourceType

# Import Celery task needed to do the real work
from tasks.tasks import virustotal_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.DOMAIN,
]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Search a domain in VirusTotal"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "vt_domain"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


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
                "plugin_name": Plugin.name,
            }

            virustotal_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))
