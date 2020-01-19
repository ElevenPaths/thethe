from celery import Celery
from celery.result import AsyncResult

celery_app = Celery(
    "tasks", backend="redis://redis", broker="redis://redis:6379/0", include=['server.plugins.dns', 'server.plugins.pastebin', 'server.plugins.shodan', 'server.plugins.whois', 'server.plugins.geoip', 'server.plugins.abuseipdb', 'server.plugins.basic_ip', 'server.plugins.binaryedge', 'server.plugins.botscout', 'server.plugins.robtex', 'server.plugins.emailrep', 'server.plugins.diario', 'server.plugins.haveibeenpwned', 'server.plugins.hunterio', 'server.plugins.maltiverse', 'server.plugins.onyphe', 'server.plugins.phishtank', 'server.plugins.sherlock', 'server.plugins.tacyt', 'server.plugins.urlscan', 'server.plugins.virustotal', 'server.plugins.verifymail', 'server.plugins.threatminer', 'server.plugins.threatcrowd', 'server.plugins.otx']
)

