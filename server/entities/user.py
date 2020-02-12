import bson

from server.db import DB
from server.entities.project import Project


class User:
    def __init__(self, user_id):
        self.user_id = bson.ObjectId(user_id)
        self.db = DB("users")

    def get_active_project(self):
        result = self.db.collection.find_one(
            {"_id": self.user_id}, {"active_project": 1}
        )

        if not "active_project" in result:
            return None

        return Project(result["active_project"])

    def set_active_project(self, project_id):
        project_id = bson.ObjectId(project_id)
        return self.db.collection.find_one_and_update(
            {"_id": self.user_id}, {"$set": {"active_project": project_id}}
        )

    # TODO: Make a route when user is switching back to project selection or logout
    def reset_active_project(self):
        project_id = bson.ObjectId(project_id)
        return self.db.collection.find_one_and_update(
            {"_id": self.user_id}, {"$set": {"active_project": None}}
        )

    def add_project(self, project_id):
        self.__project_refs(project_id, "$addToSet")

    def remove_project(self, project_id):
        self.__project_refs(project_id, "$pull")

    def __project_refs(self, project_id, operation):
        project_id = bson.ObjectId(project_id)
        return self.db.collection.find_one_and_update(
            {"_id": self.user_id}, {operation: {"project_refs": project_id}}
        )

    def get_projects(self):
        return self.db.collection.find_one({"_id": self.user_id}, {"project_refs": 1})[
            "project_refs"
        ]
