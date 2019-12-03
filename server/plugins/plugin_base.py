from enum import Enum


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
