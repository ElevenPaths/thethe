import traceback

import server.utils.password as utils
import server.utils.tokenizer as tokenizer

from server.db import DB
from flask import Blueprint, request, jsonify

authentication_api = Blueprint("authentication", __name__)


@authentication_api.route("/api/auth", methods=["POST"])
def auth():
    try:
        username = request.json["data"]["username"]
        password = request.json["data"]["password"]
        db = DB("users")
        cursor = db.collection.find_one({"username": username})
        if cursor:
            password_hash = cursor["password"]
            if utils.verify_password(password, password_hash):
                token = tokenizer.generate_auth_token(str(cursor["_id"]))
                return jsonify({"token": token.decode("utf-8"), "username": username})
        else:
            return jsonify({"error_message": "Bad user or password"}), 400

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return jsonify({"error_message": "Exception at authentication"}), 400
