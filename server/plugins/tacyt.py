import traceback
from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from tasks.tasks import celery_app

from tasks.deps.tacyt import TacytApp as tacytsdk
from tasks.api_keys import KeyRing
from server.entities.plugin_result_types import PluginResultStatus


# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.HASH]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Search an APK in Tacyt and retrieve all its info"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "tacyt"
PLUGIN_DISABLE = False
PLUGIN_NEEDS_API_KEY = True

APP_ID = KeyRing().get("tacyt-appid")
SECRET_KEY = KeyRing().get("tacyt-secret")
API_KEY_IN_DDBB = bool(APP_ID) & bool(SECRET_KEY)
API_KEY_DOC = "https://tacyt.elevenpaths.com/"
API_KEY_NAMES = ["tacyt-appid", "tacyt-secret"]


class Plugin:
    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "apk_hash": self.resource.get_data()["hash"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            tacyt.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


__OUT_FIELDS = [
    "title",
    "platform",
    "origin",
    "categoryName",
    "size",
    "marketSize",
    "numDownloads",
    "versionCode",
    "packageName",
    "price",
    "versionString",
    "minSdkVersion",
    "targetSdkVersion",
    "nFiles",
    "nImages",
    "nPermissions",
    "nMetadataApiKeys",
    "nActivities",
    "nActivityAlias",
    "nServices",
    "nReceivers",
    "nProviders",
    "nAdNetworks",
    "nAdNetworks",
    "nClassNames",
    "nMethodNames",
    "nDomains",
    "nDeveloperDomains",
    "nEmailDomains",
    "nURIDomains",
    "md5",
    "sha256",
    "hashPath",
    "recentChanges",
    "description",
    "androidXMLManifest",
    "permissionName",
    "certificateFingerprint",
    "certificateIssuerCommonName",
    "certificateIssuerCountryName",
    "certificateIssuerState",
    "certificateIssuerLocality",
    "certificateIssuerOrganizationName",
    "certificateIssuerOrganizationUnitName",
    "certificatePublicKey",
    "certificatePublicKeyInfo",
    "certificateSignatureAlgorithm",
    "certificateAutoSigned",
    "certificateSubjectCommonName",
    "certificateSubjectCountryName",
    "certificateSubjectState",
    "certificateSubjectLocality",
    "certificateSubjectOrganizationName",
    "certificateSubjectOrganizationUnitName",
    "certificateSerialNumber",
    "certificateValidityGapSeconds",
    "certificateVersion",
    "certificateValidityGapRoundedYears",
    "certificateValidFrom",
    "certificateValidTo",
    "links",
    "manifestHeaderBuiltBy",
    "manifestHeaderVersion",
    "manifestHeaderCreatedBy",
    "URIDomains",
    "emailDomains",
]


@celery_app.task
def tacyt(plugin_name, project_id, resource_id, resource_type, apk_hash):
    application = None
    result_status = PluginResultStatus.STARTED

    try:
        APP_ID = KeyRing().get("tacyt-appid")
        SECRET_KEY = KeyRing().get("tacyt-secret")
        API_KEY_IN_DDBB = bool(APP_ID) & bool(SECRET_KEY)
        if not API_KEY_IN_DDBB:
            print("No App ID key...!")
            result_status = PluginResultStatus.NO_API_KEY
        else:
            api = tacytsdk.TacytApp(APP_ID, SECRET_KEY)
            search = api.search_apps(query=apk_hash, outfields=__OUT_FIELDS)

            if (
                search.data
                and search.data.get("data")
                and search.data.get("data").get("result")
                and search.data.get("data").get("result").get("numResults") == 1
            ):
                application = (
                    search.data.get("data").get("result").get("applications")[0]
                )
                result_status = PluginResultStatus.COMPLETED
            else:
                result_status = PluginResultStatus.RETURN_NONE

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(
                plugin_name, project_id, application, result_status
            )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        application = None
