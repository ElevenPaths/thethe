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

resources_api = Blueprint("resources", __name__)


@resources_api.route("/api/create_resource", methods=["POST"])
@token_required
def create_resource(user):
    try:
        resource_name = request.json["resource_name"].strip()
        resource_type = request.json["resource_type"].lower()

        resource_type = ResourceType.get_type_from_string(resource_type)

        resource, created = ResourceManager.get_or_create(resource_name, resource_type)

        project = User(user).get_active_project()
        project.add_resource(resource)

        response = []
        response.append(
            {
                "success_message": f"Added new resource: {resource_name}",
                "new_resource": resource.to_JSON(),
                "type": resource.get_type_value(),
            }
        )

        if created:
            resource.launch_plugins(project.get_id())

        # Deal with the case of URL resources where we have the chance to add a Domain or IP
        if resource.get_type() == ResourceType.URL:
            ip_or_domain = urllib.parse.urlparse(resource_name).netloc
            resource_type = ResourceType.validate_ip_or_domain(ip_or_domain)
            if ip_or_domain:
                resource, created = Resources.get_or_create(ip_or_domain, resource_type)
                project.add_resource(resource)
                response.append(
                    {
                        "success_message": f"Added new resource: {ip_or_domain}",
                        "new_resource": resource.to_JSON(),
                        "type": resource.get_type_value(),
                    }
                )
                if created:
                    resource.launch_plugins(project.get_id())

        # TODO: Deal with the case of domain -> IP
        # TODO: Deal with the case of emails -> domains -> IP

        return jsonify(response)

    except ResourceTypeException:
        return jsonify({"error_message": "Trying to add an unknown resource type"}), 400

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return jsonify({"error_message": "Server error :("}), 400


@resources_api.route("/api/get_resources", methods=["POST"])
@token_required
def get_resources(user):
    resource_type_as_string = request.json["type"]

    try:
        resource_type = ResourceType(resource_type_as_string)

        project = User(user).get_active_project()
        resources = project.get_resources(resource_type)

        results = []
        for resource in resources:
            results.append(ResourceManager.get(resource).to_JSON())

        return jsonify(results)

    except ValueError:
        raise ResourceTypeException()

    except ResourceTypeException:
        return jsonify({"error_message": "Received an unknown type of resource"}), 400

    except Exception as e:
        print(f"Error getting resource list {e}")
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return jsonify({"error_message": "Error getting resources"}), 400


@resources_api.route("/api/unlink_resource", methods=["POST"])
@token_required
def unlink_resource(user):
    """
        Unlink (not remove) a resource from the active project.
    """
    try:
        resource_id = bson.ObjectId(request.json["resource_id"])

        project = User(user).get_active_project()
        project.remove_resource(resource_id)

        return jsonify({"success_message": "Resource unlinked from project"})

    except Exception as e:
        print(e)
        return jsonify({"error_message": "Error unlinking resource from project"}), 400


@resources_api.route("/api/get_resource", methods=["POST"])
@token_required
def get_resource(user):
    """
        Return a resource json dump by its ID
    """

    resource_id = request.json["resource_id"]

    try:
        resource = ResourceManager.get(resource_id)
        if resource:
            return jsonify(resource.to_JSON())
        else:
            return jsonify({"error_message": "Resource not found"})

    except ValueError:
        raise ResourceTypeException()

    except ResourceTypeException:
        return jsonify({"error_message": "Received an unknown type of resource"}), 400

    except Exception as e:
        print(f"Error getting ip list {e}")
        return jsonify({"error_message": "Error getting resources"}), 400
