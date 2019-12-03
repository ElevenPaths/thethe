import traceback

from ipwhois import IPWhois


def asn(ip):
    try:
        results = {}
        target = IPWhois(ip)
        lookup = target.lookup_rdap(depth=1)
        if lookup:
            results["asn"] = {
                "asn": lookup["asn"],
                "asn_cidr": lookup["asn_cidr"],
                "asn_country_code": lookup["asn_country_code"],
                "asn_date": lookup["asn_date"],
                "asn_description": lookup["asn_description"],
                "asn_registry": lookup["asn_registry"],
            }

            results["network"] = {
                "cidr": lookup["network"]["cidr"],
                "country": lookup["network"]["country"],
                "handle": lookup["network"]["handle"],
                "name": lookup["network"]["name"],
            }

        return results

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
