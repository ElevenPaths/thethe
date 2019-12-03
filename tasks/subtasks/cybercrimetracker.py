import traceback
import json
import requests, base64
from bs4 import BeautifulSoup

#from tasks.api_keys import KeyRing

#API_KEY = KeyRing().get("hybrid")

URL = "http://cybercrime-tracker.net/index.php?search={ip}"

def cybercrime_search(ip):
    try:
                
        response = {}

        headers = { "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0" }        

        response = requests.get(URL.format(**{"ip": ip}), headers=headers)
        if not response.status_code == 200:
            print("Response Service error!")
            return None
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            #response = json.loads(response.content)
            

        return soup

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None

#print ( cybercrime_search("5.79.66.145") )
