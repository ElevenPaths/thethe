# Put your Python standard libraries below this comment
import traceback

# Put your external dependencies here


# [OPTIONAL] - Does your plugin need API-Keys?
from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("YOUR_PLUGIN_NAME")


# [DONOTDELETE] - Internal usage dependencies
from server.entities.resource_types import ResourceType
from server.entities.plugin_base import finishing_task
from tasks.tasks import celery_app


"""
    RESOURCE_TARGET

    What kind of resource can this plugin handle on?

    Choices are:

        Resource.Type.DOMAIN
        Resource.Type.HASH
        Resource.Type.IPv4
        Resource.Type.URL
        Resource.Type.USERNAME

"""

# Example:
RESOURCE_TARGET = [ResourceType.DOMAIN, ResourceType.EMAIL]


"""

    PLUGIN_NAME

        A name for your plugin. Do not use spaces or non-alphanumerics symbols.

    PLUGIN_DESCRIPTION

        One line description of your plugin main functionality. Be brief.

"""

# Example:
PLUGIN_NAME = "plugin_name"
PLUGIN_DESCRIPTION = "Lists all the people working in a company with their name and email address found on the web"


"""

    PLUGIN_IS_ACTIVE = True

        True means the plugin works by "calling" directly to the target resource.

    PLUGIN_AUTOSTART = False

        If True, the plugin will be automatically run when a new resource is added.

    PLUGIN_DISABLE = False

        If True, the plugin neither will be loaded nor will be shown in thethe. Use for development.

    PLUGIN_NEEDS_API_KEY = True

        If True, there is a api key in database, false is there is not api key.

"""

PLUGIN_IS_ACTIVE = False
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False
PLUGIN_NEEDS_API_KEY = True


"""

    YOUR CONSTANTS

        Put here your CONSTS. Stuff like:

            API_ENDPOINT = "https://api.endpoint.com/v2/"

        etc.

"""

API_ENDPOINT = "https://api.endpoint.com/v2/"


"""
    Main class. A container for metadata and main action.

    In a 99% percent of cases you would not touch this.

"""


class Plugin:
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    autostart = PLUGIN_AUTOSTART

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "target": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            main.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


"""
    Main function.

        This is the function where all magic have to happen.

        If your plugin works in a different way for each resource type it
        handle do it like the snippet below.


"""


@celery_app.task
def main(plugin_name, project_id, resource_id, resource_type, target):
    try:
        query_result = None

        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = auxiliary_function_1(target)
        elif resource_type == ResourceType.EMAIL:
            query_result = auxiliary_function_2(target)
        else:
            print(f"[{PLUGIN_NAME}]: Resource type does not found")

        finishing_task(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


"""
    Auxiliary functions.

        If you need (and you will) more functions feel free to put it below.
        Do not forget to NOT decorate them like main with @celery_app.task

"""


def auxiliary_function_1(target):
    # requests.get(API_ENDPOINT) ...
    pass


def auxiliary_function_2(target):
    # requests.get(API_ENDPOINT) ...
    pass
