import json
import time
import traceback

import bson
import whois
from celery import Celery
from celery.result import AsyncResult

from server.entities.resource import Resources, ResourceType
from server.utils import password

from tasks.subtasks.abuseipdb import abuseipdb
from tasks.subtasks.asn import asn
from tasks.subtasks.binaryedge import binaryedge
from tasks.subtasks.botscout import botscout_ip
from tasks.subtasks.diario import diario
from tasks.subtasks.dns import dns
from tasks.subtasks.emailrep import emailrep
from tasks.subtasks.geoip import geoip
from tasks.subtasks.googlesearch import restricted_googlesearch
from tasks.subtasks.haveibeenpwned import haveibeenpwned
from tasks.subtasks.hunterio import hunterio_domain, hunterio_email
from tasks.subtasks.maltiverse import (
    maltiverse_domain,
    maltiverse_hash,
    maltiverse_ip,
    maltiverse_url,
)
from tasks.subtasks.onyphe import onyphe_threatlist
from tasks.subtasks.pastebin import pastebin
from tasks.subtasks.phishtank import phishtank_check
from tasks.subtasks.ptr import ptr
from tasks.subtasks.robtex import robtex
from tasks.subtasks.sherlock import sherlock
from tasks.subtasks.shodan import shodan
from tasks.subtasks.tacyt import tacyt
from tasks.subtasks.threatcrowd import (
    threatcrowd_domain,
    threatcrowd_email,
    threatcrowd_hash,
    threatcrowd_ip,
)
from tasks.subtasks.threatminer import threatminer_domain
from tasks.subtasks.urlscan import urlscan
from tasks.subtasks.verifymail import verifymail
from tasks.subtasks.virustotal import virustotal

celery_app = Celery(
    "tasks", backend="redis://localhost", broker="redis://localhost:6379/0"
)


# TODO: [URGENT] See if we can create a unified interface for a generic Celery function


@celery_app.task
def pastebin_task(
    plugin_name, project_id, resource_id, resource_type, target, search_engine
):
    try:
        # We use "googlesearch" subtask to gather results as pastebin.com does not
        # have a in-search engine
        query_result = restricted_googlesearch(search_engine, target)

        # Now, process google results and get the pastes and metadata
        if query_result:
            query_result = pastebin(query_result)

        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def geoip_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = geoip(ip)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def abuseipdb_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = abuseipdb(ip)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def robtex_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = robtex(ip)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def shodan_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = shodan(ip)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def hunterio_task(plugin_name, project_id, resource_id, resource_type, target):
    try:
        query_result = None

        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = hunterio_domain(target)
        elif resource_type == ResourceType.EMAIL:
            query_result = hunterio_email(target)
        else:
            print("Hunter.io resource type does not found")

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def threatcrowd_task(plugin_name, project_id, resource_id, resource_type, target):
    try:
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.IPv4:
            query_result = threatcrowd_ip(target)
        elif resource_type == ResourceType.DOMAIN:
            query_result = threatcrowd_domain(target)
        elif resource_type == ResourceType.EMAIL:
            query_result = threatcrowd_email(target)
        elif resource_type == ResourceType.HASH:
            query_result = threatcrowd_hash(target)
        else:
            print("ThreatCrowd resource type does not found")

        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def maltiverse_task(plugin_name, project_id, resource_id, resource_type, target):
    try:
        query_result = None
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.IPv4:
            query_result = maltiverse_ip(target)
        elif resource_type == ResourceType.DOMAIN:
            query_result = maltiverse_domain(target)
        elif resource_type == ResourceType.URL:
            query_result = maltiverse_url(target)
        elif resource_type == ResourceType.HASH:
            query_result = maltiverse_hash(target)
        else:
            print("Maltiverse resource type does not found")

        if not query_result:
            return

        print(query_result)

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def whois_task(plugin_name, project_id, resource_id, resource_type, domain):

    try:
        query_result = json.loads(str(whois.whois(domain)))
        resource_type = ResourceType(resource_type)
        # TODO: See if ResourceType.__str__ can be use for serialization
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except whois.parser.PywhoisError:
        print(f"Domain {domain} does not exists")

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


@celery_app.task
def dns_task(plugin_name, project_id, resource_id, resource_type, domain):

    query_result = {}

    # PTR
    try:
        dns_results = dns(domain)
        query_result = dns_results

        # TODO: Probably, we can save some parameters here when object is instantiated
        resource_type = ResourceType(resource_type)

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def urlscan_task(plugin_name, project_id, resource_id, resource_type, url):
    try:
        query_result = urlscan(url)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def sherlock_task(plugin_name, project_id, resource_id, resource_type, username):
    try:
        query_result = sherlock(username)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def emailrep_task(plugin_name, project_id, resource_id, resource_type, email):
    try:
        query_result = emailrep(email)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def verifymail_task(plugin_name, project_id, resource_id, resource_type, email):
    try:
        query_result = verifymail(email)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def haveibeenpwned_task(plugin_name, project_id, resource_id, resource_type, email):
    try:
        query_result = haveibeenpwned(email)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def diario_task(plugin_name, project_id, resource_id, resource_type, hash):
    try:
        query_result = diario(hash)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def tacyt_task(plugin_name, project_id, resource_id, resource_type, hash):
    try:
        query_result = tacyt(hash)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def onyphe_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = onyphe_threatlist(ip)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def phishtank_task(plugin_name, project_id, resource_id, resource_type, url):
    try:
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.URL:
            query_result = phishtank_check(url)
        else:
            print("phishtank resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def threatminer_task(plugin_name, project_id, resource_id, resource_type, domain):
    try:
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = threatminer_domain(domain, "1")
        else:
            print("threatminer resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def binaryedge_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = {}
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = binaryedge(ip)
        else:
            print("threatminer resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def botscout_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN:
            query_result = botscout_ip(ip)
        else:
            print("BotScout resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def puslsedive_task(
    plugin_name, project_id, resource_id, resource_type, domain_or_hash
):
    try:
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.DOMAIN or resource_type == ResourceType.HASH:
            query_result = pulsedive_get_ioc_byvalue(domain_or_hash)
        else:
            print("PulseDive resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def otx_task(plugin_name, project_id, resource_id, resource_type, target):
    try:
        resource_type = ResourceType(resource_type)
        # Check 2nd parameter if it's sent through view (frontend)
        if resource_type == ResourceType.IPv4:
            query_result = otx_iocs_ipv4(target, "general")
        elif resource_type == ResourceType.DOMAIN:
            query_result = otx_iocs_hostname(target, "general")
        elif resource_type == ResourceType.URL:
            query_result = otx_iocs_url(target, "general")
        elif resource_type == ResourceType.HASH:
            query_result = otx_iocs_file(target, "analysis")
        else:
            print("OTX resource type does not found")

        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))


@celery_app.task
def virustotal_task(plugin_name, project_id, resource_id, resource_type, target):
    try:
        query_result = None

        resource_type = ResourceType(resource_type)
        query_result = virustotal(target, resource_type)

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
