import traceback
import json
import bson
import time

from server.db import DB
from server.plugins.plugins import Plugins
from server.entities.update_central import UpdateCentral


class ResourceBase:
    def __init__(self, resource_id, resource_type):
        self.resource_id = bson.ObjectId(resource_id)
        self.type = resource_type

    def collection(self):
        return DB(self.get_type_value()).collection

    def get_id(self):
        return self.resource_id

    def get_id_as_string(self):
        return str(self.resource_id)

    def get_type(self):
        return self.type

    def get_type_value(self):
        return self.type.value

    def get_data(self):
        return DB(self.get_type_value()).collection.find_one({"_id": self.resource_id})

    def launch_plugins(self, project_id, profile=None):
        try:
            Plugins(self, project_id).launch_all()

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    def launch_plugin(self, project_id, plugin_name, profile=None):
        try:
            return Plugins(self, project_id).launch(plugin_name)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    def set_plugin_results(
        self, plugin_name, project_id, resource_id, resource_type, query_result
    ):
        # TODO: Should we store an time-based diff of results if they differ?
        print(plugin_name)
        print(query_result)
        result_exists = self.collection().find_one(
            {"_id": self.resource_id, f"plugins.name": plugin_name}
        )

        if not result_exists:
            self.collection().update_one(
                {"_id": self.resource_id},
                {
                    "$addToSet": {
                        "plugins": {
                            "name": plugin_name,
                            "results": query_result,
                            "creation_time": time.time(),
                            "update_time": time.time(),
                        }
                    }
                },
            )

        else:
            for plugin in result_exists["plugins"]:
                if plugin["name"] == plugin_name:
                    plugin["results"] = query_result
                    plugin["update_time"] = time.time()

            self.collection().replace_one({"_id": self.resource_id}, result_exists)

        UpdateCentral().set_pending_update(
            project_id, resource_id, resource_type, plugin_name
        )

    def get_plugins(self, project_id):
        try:
            return Plugins(self, project_id).get_plugins()

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    def manage_tag(self, tag):
        try:
            resource = self.collection().find_one({"_id": self.get_id()})

            if "tags" in resource:
                if tag["name"] in [t["name"] for t in resource["tags"]]:
                    resource["tags"] = [
                        t for t in resource["tags"] if not t["name"] == tag["name"]
                    ]
                else:
                    resource["tags"].append(
                        {"name": tag["name"], "color": tag["color"]}
                    )
            else:
                resource["tags"] = [tag]

            self.collection().replace_one({"_id": self.resource_id}, resource)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    def to_JSON(self):
        """
            Get the doc from DB and returns a JSON without the ObjectId
            Client must JSON.parse() it in browser before passing it to Vuex
        """

        def get_doc_if_reference(plugin_name, entry):
            if bson.ObjectId.is_valid(entry):
                entry = DB(plugin_name + "s").collection.find_one(
                    {"_id": entry}, {"content": 0}
                )
            return entry

        doc = DB(self.get_type_value()).collection.find_one({"_id": self.resource_id})
        # HACK:  Curiously, this seens to work in order to eliminated the double "" JSON encoding
        #       when converting from ObjectId to String

        for plugin in doc["plugins"]:
            if "results" in plugin and isinstance(plugin["results"], list):
                plugin["results"] = [
                    get_doc_if_reference(plugin["name"], entry)
                    for entry in plugin["results"]
                ]
        return json.loads(json.dumps(doc, default=str))
