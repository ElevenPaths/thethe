import traceback
from server.entities.resource_types import ResourceType
from server.entities.resource_manager import ResourceManager

# TODO: Unused base class. Either deleted it or refactor plugins base class
class PluginBase:
    def __init__(self, resource, project_id):
        """
            Base class for plugins
            Loads args from its children
        """
        self.resource = resource
        self.project_id = project_id
        self.resource_id = resource.get_id_as_string()
        self.resource_type = resource.get_type_value()


def finishing_task(plugin_name, project_id, resource_id, resource_type, result):
    try:
        if not result:
            print(
                f"[!] Plugin {plugin_name} for resource {resource_id} didn't return a result"
            )
            return

        print(result)

        resource = ResourceManager.get(resource_id)
        resource.set_plugin_results(plugin_name, project_id, result)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
