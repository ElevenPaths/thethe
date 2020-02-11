import os
import time
import bson
import json
import traceback
import urllib.parse
import importlib

from flask import Blueprint, request, abort, jsonify

from server.utils.password import token_required

from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType, ResourceTypeException
from server.entities.user import User
from server.entities.pastebin_manager import PastebinManager
from server.entities.plugin_manager import PluginManager

plugins_api = Blueprint("plugins", __name__)


@plugins_api.route("/api/get_all_plugins", methods=["POST"])
@token_required
def get_all_plugins(user):
    try:
        plugin_names = PluginManager.get_plugin_names()
        return json.dumps(plugin_names)

    except Exception as e:
        print(f"[get_all_plugins]: {e}")
        return jsonify({"error_message": "Error gettings plugins"}), 400


@plugins_api.route("/api/get_related_plugins", methods=["POST"])
@token_required
def get_related_plugins(user):
    try:
        resource_id = bson.ObjectId(request.json["resource_id"])
        resource_type_as_string = request.json["resource_type"]
        plugin_list = PluginManager.get_plugins_for_resource(resource_type_as_string)

        return json.dumps(plugin_list, default=str)

    except Exception as e:
        print(f"[get_related_plugins]: {e}")
        return jsonify({"error_message": "Error getting related plugins"}), 400


@plugins_api.route("/api/launch_plugin", methods=["POST"])
@token_required
def launch_plugin(user):
    try:
        resource_id = bson.ObjectId(request.json["resource_id"])
        plugin_name = request.json["plugin_name"]

        project = User(user).get_active_project()
        resource = Resource(resource_id)

        resource.launch_plugin(project.get_id(), plugin_name)
        return jsonify({"sucess_message": "ok"})

    except Exception as e:
        print(f"[launch_plugin]: {e}")
        return jsonify({"error_message": "Error launching plugin"}), 400


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
