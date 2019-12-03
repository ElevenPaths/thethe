import bson
import time

from server.db import DB


class UpdateCentral:
    def __init__(self):
        self.db = DB("update")

    def set_pending_update(self, project_id, resource_id, resource_type, plugin_name):
        project_id = bson.ObjectId(project_id)

        self.db.collection.insert_one(
            {
                "project_id": project_id,
                "resource_id": resource_id,
                "resource_type": resource_type.value,
                "plugin_name": plugin_name,
                "timestamp": time.time(),
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
                    "resource_type": update["resource_type"],
                }
            )

        self.db.collection.delete_many(
            {"project_id": project_id, "timestamp": {"$lte": timestamp}}
        )

        return updates
