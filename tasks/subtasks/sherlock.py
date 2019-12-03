import os
import json
import traceback

import tasks.deps.sherlock.sherlock as _sherlock


def sherlock(username):
    try:
        site_data_all = None
        data_file_path = os.path.join(
            os.getcwd(), "tasks", "deps", "sherlock", "data.json"
        )

        if site_data_all is None:
            # Check if the file exists otherwise exit.
            if not os.path.exists(data_file_path):
                print("JSON file at doesn't exist.")
                print(
                    "If this is not a file but a website, make sure you have appended http:// or https://."
                )
                return None
            else:
                raw = open(data_file_path, "r", encoding="utf-8")
                try:
                    site_data_all = json.load(raw)
                except:
                    print("Invalid JSON loaded from file.")

        result = _sherlock.sherlock(username, site_data_all, print_found_only=False)

        response = []
        for service in result:
            temp_result = {}
            temp_result["sitename"] = service
            temp_result["exists"] = result.get(service).get("exists")
            temp_result["url_user"] = result.get(service).get("url_user")
            response.append(temp_result)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
