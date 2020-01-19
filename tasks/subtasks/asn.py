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

@celery_app.task
def basic_ip_task(plugin_name, project_id, resource_id, resource_type, ip):

    query_result = {}

    # PTR
    try:
        PTR_record = ptr(ip)

        if PTR_record:
            query_result["ptr"] = PTR_record

        ASN_NET_record = asn(ip)

        if "asn" in ASN_NET_record:
            query_result["asn"] = ASN_NET_record["asn"]

        if "network" in ASN_NET_record:
            query_result["network"] = ASN_NET_record["network"]

        # TODO: Probably, we can save some parameters here when object is instantiated
        resource_type = ResourceType(resource_type)

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


