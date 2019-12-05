# Login with the following information:
# Login Name: zigineki@getnada.com
# Password: 6aiIRgAm
# The BotScout Team
# http://BotScout.com


import traceback
import json
import urllib.request
from bs4 import BeautifulSoup

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("botscout")


def botscout_ip(ip):
    try:
        URL = f"http://botscout.com/test/?ip={ip}&key={API_KEY}&format=xml"
        response = urllib.request.urlopen(URL).read()
        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


# parsing results
def botscout_ip_details(ip):
    try:
        URL = f"http://botscout.com/search.htm?sterm={ip}&stype=q"
        response = urllib.request.urlopen(URL).read()

        # parser HTML to extract last or To 10
        # soup = BeautifulSoup(response, 'html.parser')
        # html_data = soup.find('table', attrs={'class':'sortable'})
        # table_data = [[cell.text for cell in row("td")]]
        #                         for row in soup.body.find_all('table', attrs={'class' : 'sortable'})]

        # print(json.dumps(dict(table_data)))

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
