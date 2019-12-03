import traceback
import pprint
import time

import requests

from tasks.api_keys import KeyRing
from server.db import DB
from server.entities.pastebin_manager import PastebinManager, Paste


API_KEY = KeyRing().get("pastebin")
# pastebin.com says 1 second between queries, so be cautious and lets it be 1.1 seconds
# https://pastebin.com/doc_scraping_api#5
RATE_LIMIT = 1.1

METADATA_URL = "https://scrape.pastebin.com/api_scrape_item_meta.php?i="
RAWPASTE_URL = "https://scrape.pastebin.com/api_scrape_item.php?i="


def get_key_from_paste_key(item):
    return item.split("/")[-1]


def pastebin(results):
    try:
        if not API_KEY:
            raise Exception("No API_KEY for pastebin")

        links = []
        if "items" in results:
            links = [item["link"] for item in results["items"]]
        pastebins_refs = []

        for link in links:
            paste_key = get_key_from_paste_key(link)
            try:
                time.sleep(RATE_LIMIT)

                args = {}
                meta = requests.get(METADATA_URL + paste_key)
                if meta.status_code == 200:
                    try:
                        meta = meta.json()[0]
                    except:
                        print(f"This paste {paste_key} has been deleted")
                        continue
                else:
                    print(f"Error {meta.status_code} getting paste from pastebin.com")
                    continue

                for field in [
                    "size",
                    "title",
                    "user",
                    "hits",
                    "date",
                    "syntax",
                    "expire",
                ]:
                    args[field] = meta[field]

                paste = Paste(paste_key, args)

                time.sleep(RATE_LIMIT)

                result = requests.get(RAWPASTE_URL + paste_key)

                if result.status_code == 200:
                    paste.set_content(result.content)

                pastebins_refs.append(paste.save())

            except Exception as e:
                print(f"Failed to get pastebin: {link}")
                tb1 = traceback.TracebackException.from_exception(e)
                print("".join(tb1.format()))
                continue

        if len(pastebins_refs) == 0 or len(links) == 0:
            return None
        return pastebins_refs

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
