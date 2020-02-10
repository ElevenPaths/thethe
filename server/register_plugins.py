import sys

sys.path.append(".")

from server.entities.plugin_manager import register_plugins

register_plugins()
