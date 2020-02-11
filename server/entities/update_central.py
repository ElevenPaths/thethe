import bson
import time

from server.db import DB
from server.entities.plugin_result_types import PluginResultStatus


class UpdateCentral:
    def __init__(self):
        self.db = DB("update")

    def set_pending_update(self, project_id, resource_id, plugin_name, result_status):
        project_id = bson.ObjectId(project_id)

        message = ""
        status = ""

        if result_status == PluginResultStatus.NO_API_KEY:
            message = f"there is a problem with de API KEY!"
            status = "error"
        elif result_status == PluginResultStatus.RETURN_NONE:
            message = f"received no results"
            status = "info"
        elif result_status == PluginResultStatus.FAILED:
            message = f"plugin failed to run"
            status = "error"
        elif result_status == PluginResultStatus.COMPLETED:
            message = f"successfully completed"
            status = "success"

        print(f"[UpdateCentral.set_pending_update]: {status} {message}")

        self.db.collection.insert_one(
            {
                "project_id": project_id,
                "resource_id": resource_id,
                "plugin_name": plugin_name,
                "timestamp": time.time(),
                "message": message,
                "status": status,
            }
        )

    def get_pending_updates(self, project_id, timestamp):
        timestamp = timestamp
        pending_updates = self.db.collection.find(
            {"project_id": project_id, "timestamp": {"$lte": timestamp}}
        )

        updates = []
        for update in pending_updates:
            updates.append(
                {
                    "resource_id": update["resource_id"],
                    "message": update["message"],
                    "status": update["status"],
                }
            )

        self.db.collection.delete_many(
            {"project_id": project_id, "timestamp": {"$lte": timestamp}}
        )

        return updates
