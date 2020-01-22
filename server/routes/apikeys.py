import time
import bson
import json
import traceback

from bson.json_util import dumps
from flask import Blueprint, request, abort, jsonify

from server.db import DB
from server.utils.password import token_required
from server.entities.user import User

apikeys_api = Blueprint("apikeys", __name__)


@apikeys_api.route("/api/get_apikeys", methods=["POST"])
@token_required
def get_apikeys(user):
    try:
        results = DB("apikeys").collection.find({}, {'_id': False})
        list_results = list(results)

        return dumps(list_results)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error getting API keys"}), 400

@apikeys_api.route("/api/upload_apikeys", methods=["POST"])
@token_required
def upload_apikeys(user):
    try:
        apikeys = request.json["entries"]
        for apikey in apikeys:
            result = DB("apikeys").collection.update_one(
                {"name": apikey["name"]}, {"$set": {"apikey": apikey["apikey"]}}, True
            )

        return json.dumps(apikeys, default=str)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error uploading API keys"}), 400

@apikeys_api.route("/api/remove_apikeys", methods=["POST"])
@token_required
def remove_apikeys(user):
    try:
        apikeys = request.json["entries"]
        for name in apikeys:
            print(name)
            result = DB("apikeys").collection.remove(
                {"name": name["name"]}
            )

        return json.dumps(apikeys, default=str)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error removing API keys"}), 400
