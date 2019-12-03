import traceback

from tasks.deps.tacyt import TacytApp as tacytsdk
from tasks.api_keys import KeyRing


APP_ID = KeyRing().get("tacyt-appid")
SECRET_KEY = KeyRing().get("tacyt-secret")

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


def tacyt(_hash):
    application = None
    try:
        api = tacytsdk.TacytApp(APP_ID, SECRET_KEY)
        search = api.search_apps(query=_hash, outfields=__OUT_FIELDS)

        if (
            search.data
            and search.data.get("data")
            and search.data.get("data").get("result")
            and search.data.get("data").get("result").get("numResults") == 1
        ):
            application = search.data.get("data").get("result").get("applications")[0]
        return application

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        application = None

    return application
