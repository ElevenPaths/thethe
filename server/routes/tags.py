import time
import bson
import json
import traceback
import urllib.parse


from flask import Blueprint, request, abort, jsonify

from server.utils.password import token_required

from server.entities.resource_manager import ResourceManager
from server.entities.resource_types import ResourceType, ResourceTypeException
from server.entities.user import User

from server.entities.tag_manager import TagManager, AVAILABLE_COLORS

tags_api = Blueprint("tags", __name__)


@tags_api.route("/api/get_tags", methods=["POST"])
@token_required
def get_tags(user):
    try:
        tags_list = TagManager().get_tags()
        result = {"tags": json.loads(json.dumps(tags_list, default=str))}
        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error getting global tags"}), 400


@tags_api.route("/api/add_new_tag", methods=["POST"])
@token_required
def add_new_tag(user):
    try:
        project = User(user).get_active_project()
        name = request.json["tag"]["name"]
        color = request.json["tag"]["color"]

        TagManager().new({"name": name, "color": color})

        return jsonify({"sucess_message": "ok"})

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error adding new tag"}), 400


@tags_api.route("/api/update_tag", methods=["POST"])
@token_required
def update_tag(user):
    try:

        pass
    except Exception as e:
        print(e)
        return (
            jsonify({"error_message": "Something gone wrong when getting paste"}),
            400,
        )


@tags_api.route("/api/get_tag_colors", methods=["POST"])
@token_required
def get_tag_colors(user):
    try:
        tag_colors = {"tag_colors": AVAILABLE_COLORS}
        return jsonify(tag_colors)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error getting global tags"}), 400


@tags_api.route("/api/tag_to_resource", methods=["POST"])
@token_required
def tag_to_resource(user):
    try:
        resource_id = bson.ObjectId(request.json["resource_id"])
        resource_type_as_string = request.json["resource_type"]
        tag = request.json["tag"]

        resource_type = ResourceType(resource_type_as_string)
        resource = ResourceManager.get(resource_id)
        resource.manage_tag(tag)

        return jsonify({"sucess_message": "ok"})

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error getting global tags"}), 400
