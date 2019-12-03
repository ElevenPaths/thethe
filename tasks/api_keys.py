from server.db import DB


class KeyRing:
    def __init__(self):
        self.db = DB("apikeys")
        self.keyring = DB("apikeys").collection.find()

    def get(self, name):
        for entry in self.keyring:
            if entry["name"] == name:
                return entry["apikey"]
        return None

    def new(self, name, apikey):
        self.db.insert_one({"name": name, "apikey": apikey})

    def update(self, name, apikey):
        entry = self.get(name)
        if entry:
            self.db.update_one({"_id": entry["_id"]}, {"apikey": apikey})
