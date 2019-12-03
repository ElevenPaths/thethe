from dns import resolver, reversename


def ptr(ip):
    try:
        PTR_record = None
        addr = reversename.from_address(ip)
        PTR_record = str(resolver.query(addr, "PTR")[0])
        return PTR_record
    except Exception as e:
        print(e)
        return None
