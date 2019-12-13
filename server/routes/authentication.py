import traceback
import bson

import server.utils.password as utils
import server.utils.tokenizer as tokenizer

from server.db import DB
from server.utils.password import token_required, hash_password
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


@authentication_api.route("/api/changepassword", methods=["POST"])
@token_required
def change_password(user):
    try:
        #username = request.json["username"]
        old_password = request.json["old_password"]
        new_password_1 = request.json["new_password_1"]
        new_password_2 = request.json["new_password_2"]
        user = bson.ObjectId(user)

        if not new_password_1 == new_password_2:
            print("[AUTH] Unmatched new password for change password operation")
            return jsonify({"error_message": "New password does not match"}), 400

        db = DB("users")
        cursor = db.collection.find_one({"_id": user})
        if cursor:
            password_hash = cursor["password"]
            if utils.verify_password(old_password, password_hash):
                db.collection.update({"_id": user}, {"$set": {"password": hash_password(new_password_1)}})
            return jsonify({"success_message": "Password changed"})
        else:
            return jsonify({"error_message": "Bad user or password"}), 400

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return jsonify({"error_message": "Exception at authentication"}), 400