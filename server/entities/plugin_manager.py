import os
import importlib
import traceback
import pymongo

from server.db import DB
from server.entities.resource_types import ResourceType

PLUGIN_DIRECTORY = "server/plugins/"
PLUGIN_HIERARCHY = "server.plugins"
EXCLUDE_SET = ["__init__.py", "TEMPLATE.py"]


def _get_module_names():
    """
        Get all the plugins names to load on
    """
    plugins = []
    for root, dirs, files in os.walk("server/plugins"):
        for file in files:
            if ".py" in file[-3:] and not file in EXCLUDE_SET:
                plugins.append("server.plugins.{}".format(os.path.splitext(file)[0]))
    return plugins


def register_plugins():
    """
        This function register metadata from enabled plugins upon container startup
    """
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
                    "target": [resource.value for resource in module.RESOURCE_TARGET],
                    "needs_apikey": module.PLUGIN_NEEDS_API_KEY,
                    "apikey_in_ddbb": module.API_KEY_IN_DDBB,
                    "apikey_doc": module.API_KEY_DOC,
                    "apikey_names": module.API_KEY_NAMES,
                }
            )


def _load_module(plugin_name):
    try:
        module = importlib.import_module(f"{PLUGIN_HIERARCHY}.{plugin_name}")
        return module

    except Exception as e:
        print(f"[_load_module] {e}")
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


class PluginManager:
    @staticmethod
    def get_plugin_names():
        try:
            db = DB("plugins")
            plugins = db.collection.find({"needs_apikey": True})

            non_apikeys_fields = []
            for plugin in plugins:
                non_apikeys_fields.extend(plugin["apikey_names"])

            db = DB("apikeys")
            apikeys = [apikey["name"] for apikey in db.collection.find({})]

            non_apikeys_fields = set(non_apikeys_fields) - set(apikeys)

            return list(non_apikeys_fields)

        except Exception as e:
            print(f"[PluginManager.get_plugin_names] {e}")
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    @staticmethod
    def get_autostart_plugins_for_resource(resource_type_as_string):
        try:
            db = DB("plugins")
            plugins = db.collection.find(
                {"autostart": True, "target": resource_type_as_string}
            )
            return [plugin["name"] for plugin in plugins]

        except Exception as e:
            print(f"[PluginManager.get_autostart_plugins_for_resource] {e}")
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    @staticmethod
    def get_plugins_for_resource(resource_type_as_string):
        db = DB("plugins")
        plugins = db.collection.find({"target": resource_type_as_string}).sort(
            [("name", pymongo.ASCENDING)]
        )
        results = []
        for entry in plugins:
            results.append(
                {
                    "name": entry["name"],
                    "description": entry["description"],
                    "api_key": entry["needs_apikey"],
                    "api_docs": entry["apikey_doc"],
                    "is_active": entry["is_active"],
                    "apikey_in_ddbb": entry["apikey_in_ddbb"],
                }
            )
        return results

    def __init__(self, resource, project_id):
        self.resource = resource
        self.project_id = project_id

    # TODO: Profiles are not implemented yet (11/02/2020)
    def launch_all(self, profile="pasive"):
        """
            Launch all the loaded plugins based on a profile (by default non active or noisy modules)
        """
        try:
            plugins = PluginManager.get_autostart_plugins_for_resource(
                self.resource.get_type_value()
            )
            name_list = " ".join(plugins)
            print(
                f"[PluginManager.launch_all]: Launching autostart plugins...{name_list}"
            )

            for plugin in plugins:
                module = _load_module(plugin)
                module.Plugin(self.resource, self.project_id).do()

        except Exception as e:
            print(f"[PluginManager.launch_all] {e}")
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    def launch(self, plugin_name):
        try:
            module = _load_module(plugin_name)
            print(f"Launching {module.PLUGIN_NAME}")
            return module.Plugin(self.resource, self.project_id).do()

        except Exception as e:
            print(f"[PluginManager.launch] {e}")
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))
