import os
import importlib
import traceback

from server.db import DB
from server.entities.resource_types import ResourceType

PLUGIN_DIRECTORY = "server/plugins/"
PLUGIN_HIERARCHY = "server.plugins"
EXCLUDE_SET = ["__init__.py", "TEMPLATE.py"]


def _get_module_names():
    plugins = []
    for root, dirs, files in os.walk("server/plugins"):
        for file in files:
            if ".py" in file[-3:] and not file in EXCLUDE_SET:
                plugins.append("server.plugins.{}".format(os.path.splitext(file)[0]))
    return plugins


def register_plugins():
    db = DB("plugins")
    db.collection.delete_many({})

    for module in _get_module_names():
        module = importlib.import_module(module)
        if not module.PLUGIN_DISABLE:
            print(f"registering {module.PLUGIN_NAME}")
            db.collection.insert_one(
                {
                    "name": module.PLUGIN_NAME,
                    "is_active": module.PLUGIN_IS_ACTIVE,
                    "description": module.PLUGIN_DESCRIPTION,
                    "autostart": module.PLUGIN_AUTOSTART,
                    "api_key": module.PLUGIN_API_KEY,
                    "target": [resource.value for resource in module.RESOURCE_TARGET],
                }
            )


def _load_plugins(resource_type, name=None):
    """
        Load effective plugins for this resource based on its type
    """
    plugins = []
    files = os.scandir(PLUGIN_DIRECTORY)

    for f in files:
        if f.is_file() and f.name.endswith(".py") and not f.name in EXCLUDE_SET:
            module = importlib.import_module(f"{PLUGIN_HIERARCHY}.{f.name[:-3]}")
            if resource_type in module.RESOURCE_TARGET and not module.PLUGIN_DISABLE:
                plugins.append(module.Plugin)

    return plugins


class PluginManager:
    def __init__(self, resource, project_id):
        self.resource = resource
        self.plugins = _load_plugins(resource.get_type())
        self.project_id = project_id

    def launch_all(self, profile="pasive"):
        """
            Launch all the loaded plugins based on a profile (by default non active or noisy modules)
        """
        for plugin in self.plugins:
            if plugin.autostart:
                print(f"Launching {plugin.name}")
                plugin(self.resource, self.project_id).do()

    def launch(self, plugin_name):
        try:
            for plugin in self.plugins:
                if plugin.name == plugin_name:
                    return plugin(self.resource, self.project_id).do()

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    def get_plugins(self):
        """
            Return a list of relevant plugins for a resource
        """

        def by_name(elem):
            return elem["name"]

        plugin_list = []
        for plugin in self.plugins:
            plugin = plugin(self.resource, self.project_id)
            plugin_list.append(
                {
                    "name": plugin.name,
                    "description": plugin.description,
                    "api_key": plugin.api_key,
                    "api_doc": plugin.api_doc,
                    "is_active": plugin.is_active,
                    "apikey_in_ddbb": plugin.apikey_in_ddbb,
                }
            )

        plugin_list.sort(key=by_name)
        return plugin_list
