import bson
import time
import traceback

from flask import Blueprint, request, abort, jsonify, Response

from server.db import DB
from server.utils.password import token_required

from server.entities.user import User
from server.entities.project import (
    Projects,
    ProjectExistException,
    ProjectNameException,
    ProjectNotExistsException,
)

from server.utils.desobjectid import desobjectid_cursor

projects_api = Blueprint("projects", __name__)


@projects_api.route("/api/ping", methods=["POST"])
@token_required
def ping(user):
    try:
        timestamp = time.time()
        updates = User(user).get_active_project().get_updates(timestamp)
        return jsonify(updates)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return jsonify({"error_message": "Server error :("}), 400


# TODO: Delete usage of desobjectid
@projects_api.route("/api/get_projects", methods=["POST"])
@token_required
def get_projects(user):
    try:
        projects = User(user).get_projects()
        user_projects = Projects.get_project_docs(projects, ["name", "creation_date"])
        return jsonify(desobjectid_cursor(user_projects))

    except Exception as e:
        print(f"Error when retrieving project {e}")
        return jsonify({"error_message": "Error when retrieving a project"}), 400


@projects_api.route("/api/new_project", methods=["POST"])
@token_required
def new_project(user):
    try:
        name = request.json["name"]
        project_id = Projects.create(name, user)
        User(user).add_project(project_id)

        return jsonify({"success_message": f"New project {name} created"})

    except ProjectNameException:
        print(f"Project name error")
        return (jsonify({"error_message": "Project name error"}), 400)

    except ProjectExistException:
        print(f"Project already exists in database")
        return (
            jsonify({"error_message": "A project with that name already exists"}),
            400,
        )

    except Exception as e:
        print(f"Error when creating new project {e}")
        return jsonify({"error_message": "Error when creating a new project"}), 400


@projects_api.route("/api/delete_project", methods=["POST"])
@token_required
def delete_project(user):
    try:
        project_id = request.json["project_id"]
        Projects.delete(project_id)
        User(user).remove_project(project_id)

        return jsonify({"success_message": f"Selected project deleted"})

    except ProjectNotExistsException as e:
        print(f"Selected project for deletion does not exists {e}")
        return (
            jsonify(
                {
                    "error_message": "Deletion error: Could not find any project with that ID"
                }
            ),
            400,
        )

    except Exception as e:
        print(f"Error when deleting a project {e}")
        return jsonify({"error_message": "Error during deletion"}), 400


@projects_api.route("/api/set_active_project", methods=["POST"])
@token_required
def set_active_project(user):
    try:
        project_id = request.json["project_id"]
        User(user).set_active_project(project_id)
        return jsonify({})

    except Exception as e:
        print(f"Error when setting an active project {e}")
        return jsonify({"error_message": "Error during active project setting"}), 400
