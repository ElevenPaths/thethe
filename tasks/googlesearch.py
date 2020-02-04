import traceback
import pprint
import requests

from googleapiclient.discovery import build
from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("googlesearch")

SORT = "date"
RESULTS_LIMIT = 10


def googlesearch(search_engine, keyword):
    try:
        if not API_KEY:
            raise Exception("No API_KEY")

        service = build("customsearch", "v1", developerKey=API_KEY)

        response = service.cse().list(q=keyword, cx=search_engine).execute()

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


def restricted_googlesearch(search_engine, keyword):
    # Use unlimited site restricted JSON API
    # https://developers.google.com/custom-search/v1/site_restricted_api
    try:
        URL_TEMPLATE = f"https://www.googleapis.com/customsearch/v1/siterestrict?key={API_KEY}&cx={search_engine}&q=%22{keyword}%22&sort={SORT}&num={RESULTS_LIMIT}"

        response = requests.get(URL_TEMPLATE)

        if response.status_code == 200:
            return response.json()

        else:
            return None

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
