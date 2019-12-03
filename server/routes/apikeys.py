import time
import bson
import json
import traceback

from flask import Blueprint, request, abort, jsonify

from server.db import DB
from server.utils.password import token_required
from server.entities.user import User

apikeys_api = Blueprint("apikeys", __name__)


@apikeys_api.route("/api/get_apikeys", methods=["POST"])
@token_required
def get_apikeys(user):
    try:
        results = DB("apikeys").collection.find({})
        results = [result for result in results]

        return json.dumps(results, default=str)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error getting global tags"}), 400


@apikeys_api.route("/api/upload_apikeys", methods=["POST"])
@token_required
def upload_apikeys(user):
    try:
        apikeys = request.json["entries"]
        for apikey in apikeys:
            result = DB("apikeys").collection.find_one({"name": apikey["name"]})
            if not result:
                DB("apikeys").collection.insert_one(
                    {"name": apikey["name"], "apikey": apikey["apikey"]}
                )

        return json.dumps(apikeys, default=str)

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error getting global tags"}), 400
