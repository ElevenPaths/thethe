import traceback
import json
import bson
import time
import urllib.parse


from server.db import DB
from server.plugins.plugins import Plugins
from server.entities.update_central import UpdateCentral
from server.entities.resource_types import ResourceType
from server.entities.hash_types import HashType

COLLECTION = "resources"

# TODO: Legacy method for old database resources
# TODO: Get rid of this legacy method
def get_resource_legacy_method(resource_id):
    """
        Lookup the resource_id in all old documents
        Returns resource and doc name to change global COLLECTION
    """
    docs = ["ip", "url", "username", "hash", "email", "domain"]

    for doc in docs:
        collection = DB(doc).collection
        resource = collection.find_one({"_id": resource_id})

        if resource:
            return (resource, doc)

    print(f"[resource_base/get_resource_legacy_method]: {resource_id}")

    return (None, None)


def enrich_by_type(args):
    resource_type = ResourceType(args["resource_type"])

    if resource_type == ResourceType.IPv4:
        args["address"] = args["canonical_name"]

    elif resource_type == ResourceType.USERNAME:
        args["username"] = args["canonical_name"]

    elif resource_type == ResourceType.URL:
        args["full_url"] = args["canonical_name"]

        url_parts = urllib.parse.urlparse(args["full_url"])
        args["scheme"] = url_parts.scheme
        args["netloc"] = url_parts.netloc
        args["path"] = url_parts.path
        args["params"] = url_parts.params
        args["query"] = url_parts.query
        args["fragment"] = url_parts.fragment

    elif resource_type == ResourceType.HASH:
        args["hash"] = args["canonical_name"]
        args["hash_type"] = HashType.hash_detection(args["hash"])
        # canonical_name == printable name in the view
        args["canonical_name"] = args["hash"][:8]

    elif resource_type == ResourceType.EMAIL:
        args["email"] = args["canonical_name"]
        if "@" in args["email"]:
            args["domain"] = args["email"].split("@")[1]
        else:
            args["domain"] = None

    elif resource_type == ResourceType.DOMAIN:
        args["domain"] = args["canonical_name"]

    else:
        print(
            f"[entities/resource_base/enrich_by_type]: Unknown resource type {args['resource_type']} when creating resource."
        )

    return args


class Resource:
    @staticmethod
    def collection(collection=COLLECTION):
        return DB(collection).collection

    @staticmethod
    def create(name, resource_type):
        """
            name: name of the resource
            type: type as ResourceType
        """
        args = {
            "canonical_name": name,
            "resource_type": resource_type.value,
            "creation_time": time.time(),
            "plugins": [],
            "tags": [],
        }

        args = enrich_by_type(args)
        result = Resource.collection().insert_one(args)

        return Resource(str(result.inserted_id))

    def __init__(self, resource_id):
        self.resource_id = bson.ObjectId(resource_id)
        collection = COLLECTION
        self.resource = Resource.collection(collection).find_one(
            {"_id": self.resource_id}
        )
        # TODO: Get rid of this legacy method
        # We have found anything, try legacy database method
        if not self.resource:
            # If found, change global resource database
            self.resource, collection = get_resource_legacy_method(self.resource_id)

        # Store collection name
        self.own_collection = collection

    def get_collection(self):
        return Resource.collection(self.own_collection)

    def get_id_as_string(self):
        return str(self.resource_id)

    def get_type(self):
        return ResourceType.get_type_from_string(self.resource["resource_type"])

    def get_type_value(self):
        return self.get_type().value

    def get_data(self):
        return self.resource

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

    def set_plugin_results(self, plugin_name, project_id, query_result):
        # TODO: Should we store an time-based diff of results if they differ?
        result_exists = self.get_collection().find_one(
            {"_id": self.resource_id, f"plugins.name": plugin_name}
        )

        if not result_exists:
            self.get_collection().update_one(
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

            self.get_collection().replace_one({"_id": self.resource_id}, result_exists)

        UpdateCentral().set_pending_update(
            project_id, self.get_id_as_string(), self.get_type(), plugin_name
        )

    def get_plugins(self, project_id):
        try:
            return Plugins(self, project_id).get_plugins()

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

    def manage_tag(self, tag):
        try:
            resource = self.get_collection().find_one({"_id": self.resource_id})

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

            self.get_collection().replace_one({"_id": self.resource_id}, resource)

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
                entry = self.get_collection().find_one({"_id": entry}, {"content": 0})
            return entry

        doc = self.get_collection().find_one({"_id": self.resource_id})
        # HACK:  Curiously, this seens to work in order to eliminated the double "" JSON encoding
        #       when converting from ObjectId to String

        for plugin in doc["plugins"]:
            if "results" in plugin and isinstance(plugin["results"], list):
                plugin["results"] = [
                    get_doc_if_reference(plugin["name"], entry)
                    for entry in plugin["results"]
                ]
        return json.loads(json.dumps(doc, default=str))
