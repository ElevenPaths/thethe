import os
import time
import bson
import json
import traceback
import urllib.parse
import importlib

from flask import Blueprint, request, abort, jsonify

from server.utils.password import token_required

from server.entities.resource import Resources
from server.entities.resource_types import ResourceType, ResourceTypeException
from server.entities.user import User
from server.entities.pastebin_manager import PastebinManager

plugins_api = Blueprint("plugins", __name__)


@plugins_api.route("/api/get_all_plugins", methods=["POST"])
@token_required
def get_all_plugins(user):
    try:
        PLUGIN_DIRECTORY = "server/plugins/"
        PLUGIN_HIERARCHY = "server.plugins"
        EXCLUDE_SET = ["plugins.py", "__init__.py", "plugin_base.py"]

        plugins = []
        files = os.scandir(PLUGIN_DIRECTORY)

        for f in files:
            if f.is_file() and f.name.endswith(".py") and not f.name in EXCLUDE_SET:
                module = importlib.import_module(f"{PLUGIN_HIERARCHY}.{f.name[:-3]}")
                if module.PLUGIN_API_KEY and not module.PLUGIN_DISABLE:
                    plugins.append(module.PLUGIN_NAME)

        return json.dumps(plugins)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error gettings plugins"}), 400

@plugins_api.route("/api/get_related_plugins", methods=["POST"])
@token_required
def get_plugins(user):
    try:
        resource_id = bson.ObjectId(request.json["resource_id"])
        project_id = bson.ObjectId(request.json["project_id"])
        resource_type_as_string = request.json["resource_type"]

        project = User(user).get_active_project()
        resource_type = ResourceType(resource_type_as_string)
        resource = Resources.get(resource_id, resource_type)
        plugin_list = resource.get_plugins(project_id)

        return json.dumps(plugin_list, default=str)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error unlinking resource from project"}), 400


@plugins_api.route("/api/launch_plugin", methods=["POST"])
@token_required
def launch_plugin(user):
    try:
        resource_id = bson.ObjectId(request.json["resource_id"])
        resource_type_as_string = request.json["resource_type"]
        plugin_name = request.json["plugin_name"]

        project = User(user).get_active_project()
        resource_type = ResourceType(resource_type_as_string)
        resource = Resources.get(resource_id, resource_type)

        resource.launch_plugin(project.get_id(), plugin_name)
        return jsonify({"sucess_message": "ok"})

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error unlinking resource from project"}), 400


@plugins_api.route("/api/load_paste", methods=["POST"])
@token_required
def load_paste(user):
    try:
        paste_id = bson.ObjectId(request.json["paste_id"])
        paste = PastebinManager().get_by_id(paste_id)

        if not paste:
            return jsonify({"error_message": "paste not found"}), 400

        return jsonify(paste["content"].decode("utf-8"))

    except Exception as e:
        print(e)
        return (
            jsonify({"error_message": "Something gone wrong when getting paste"}),
            400,
        )
