import traceback
import json
import requests


from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("shodan")

URL = "https://api.shodan.io/shodan/host/{ip}?key={API_KEY}"


def shodan(ip):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}
        ipinfo = requests.get(URL.format(**{"ip": ip, "API_KEY": API_KEY}))
        if not ipinfo.status_code == 200:
            return None
        else:
            ipinfo = json.loads(ipinfo.content)
            with open("/tmp/shodan.json", "w") as f:
                f.write(json.dumps(ipinfo))

        response["hostnames"] = ipinfo["hostnames"] if "hostnames" in ipinfo else []
        response["os"] = ipinfo["os"] if "os" in ipinfo else None
        response["org"] = ipinfo["org"] if "org" in ipinfo else None
        response["isp"] = ipinfo["isp"] if "isp" in ipinfo else None
        response["services"] = []

        for data in ipinfo["data"]:
            service = {}
            service["port"] = data["port"] if "port" in data else None
            service["transport"] = data["transport"] if "transport" in data else None
            service["service"] = data["service"] if "service" in data else None
            service["data"] = data["data"] if "data" in data else None
            service["product"] = data["product"] if "product" in data else None
            service["banner"] = data["banner"] if "banner" in data else None
            service["devicetype"] = data["devicetype"] if "devicetype" in data else None
            service["timestamp"] = data["timestamp"] if "timestamp" in data else None
            service["hostnames"] = data["hostnames"] if "hostnames" in data else []

            response["services"].append(service)

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
