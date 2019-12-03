import dns.resolver as resolver
import traceback

from urllib.parse import urlparse

# If you want to expand DNS query types this is the right place
LOOKUP = ["NS", "A", "AAAA", "MX", "TXT", "SRV"]


def dns(domain):
    try:
        results = {}

        for TYPE in LOOKUP:
            try:
                r = resolver.query(domain, TYPE)
                results[TYPE] = [str(i) for i in r]

            except:
                # Case when the query must be on canonical domain
                try:
                    root_name = ".".join(domain.split(".")[-2:])
                    r = resolver.query(root_name, TYPE)
                    results[TYPE] = [str(i) for i in r]

                except:
                    results[TYPE] = None

        print(results)
        return results

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
