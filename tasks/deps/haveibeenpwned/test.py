import json


def breach_detail_filler(sites):
    blob = None
    with open("breaches.json", "r") as f:
        blob = json.loads(f.read())

    if not blob:
        return []

    results = []

    sites = [site["Name"] for site in sites]

    return [entry for entry in blob if entry["Name"] in sites]


if __name__ == "__main__":
    sites = [{"Name": "Canva"}, {"Name": "Dropbox"}]
    print(breach_detail_filler(sites))
