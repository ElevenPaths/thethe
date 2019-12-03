import traceback

from passlib.apps import custom_app_context as pwd_context
from functools import wraps
from flask import request, jsonify
from server.utils import tokenizer


def hash_password(password):
    password_hash = pwd_context.hash(password)
    return password_hash


def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kargs):
        try:
            if not "Authorization" in request.headers:
                return (
                    jsonify({"error_message": "No authorization header in request"}),
                    400,
                )

            token = request.headers["Authorization"]
            user = tokenizer.verify_auth_token(token)["id"]
            return f(user, *args, **kargs)
        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))
            return jsonify({"error_message": "Insecure request"}), 400

    return decorated_function
