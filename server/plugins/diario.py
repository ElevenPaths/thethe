import traceback
import json
import requests

from diario import Diario

from server.entities.resource_base import Resource
from server.entities.resource_types import ResourceType
from server.entities.plugin_result_types import PluginResultStatus
from tasks.api_keys import KeyRing
from tasks.tasks import celery_app

__PREDICTION = {"M": "Malware", "G": "Goodware", "NM": "No macros"}
__STATUS = {"A": "Analyzed", "P": "Processing", "F": "Failed"}

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.HASH]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_AUTOSTART = False
PLUGIN_DESCRIPTION = "Scans and analyzes pdf and office documents in a static way keeping users content private"
PLUGIN_DISABLE = False
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "diario"
PLUGIN_NEEDS_API_KEY = True

APP_ID = KeyRing().get("diario-appid")
SECRET_KEY = KeyRing().get("diario-secret")
API_KEY_IN_DDBB = bool(APP_ID) & bool(SECRET_KEY)
API_KEY_DOC = "https://diario.e-paths.com"
API_KEY_NAMES = ["diario-appid", "diario-secret"]


class Plugin:
    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "document_hash": self.resource.get_data()["hash"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            diario.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))


@celery_app.task
def diario(plugin_name, project_id, resource_id, resource_type, document_hash):
    result_status = PluginResultStatus.STARTED
    result = {"is_document": False}

    try:
        if APP_ID and SECRET_KEY:
            print("No App ID key...!")
            result_status = PluginResultStatus.NO_API_KEY

        else:
            diariosdk = Diario(APP_ID, SECRET_KEY)
            response = diariosdk.search(document_hash)

            if response.data:
                result = get_result(diariosdk, response.data)
                result_status = PluginResultStatus.COMPLETED
            else:
                result_status = PluginResultStatus.RETURN_NONE

        resource = Resource(resource_id)
        if resource:
            resource.set_plugin_results(plugin_name, project_id, result, result_status)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        result = None


def get_result(diariosdk, data):
    document_type = data.get("type")
    if not document_type:
        document_type = "pdf"

    return {
        "is_document": True,
        "document_type": document_type,
        "prediction": __PREDICTION.get(data.get("prediction")),
        "status": __STATUS.get(data.get("status")),
        "sub_documents": get_subdocument(diariosdk, data, document_type),
    }


def _get_subdocument(diariosdk, data, document_type):
    sub_documents = []
    if document_type == "pdf":
        sub_document_type = "javaScripts"
    else:
        sub_document_type = "macros"

    for sub_document in data.get(sub_document_type):
        if document_type == "pdf":
            sd_response = diariosdk.get_javascript_info(sub_document)
        else:
            sd_response = diariosdk.get_macro_info(sub_document)

        if sd_response and sd_response.data:
            sub_documents.append(sd_response.data)

    return sub_documents


def get_subdocument(diariosdk, data, document_type):
    sub_documents = []
    if document_type == "pdf":
        sub_document_type = "javaScripts"
    else:
        sub_document_type = "macros"

    for sub_document in data.get(sub_document_type):
        if document_type == "pdf":
            sd_response = diariosdk.get_javascript_info(sub_document)
        else:
            sd_response = diariosdk.get_macro_info(sub_document)

        if sd_response and sd_response.data:
            sub_documents.append(sd_response.data)

    return sub_documents


def old_get_result(diariosdk, data):
    document_type = data.get("type")
    if not document_type:
        document_type = "pdf"

    return {
        "is_document": True,
        "document_type": document_type,
        "prediction": __PREDICTION.get(data.get("prediction")),
        "status": __STATUS.get(data.get("status")),
        "sub_documents": get_subdocument(diariosdk, data, document_type),
    }


def old_diario(document_hash):
    result = {"is_document": False}
    try:
        if not APP_ID:
            print("No App ID key...!")
            return None

        if not SECRET_KEY:
            print("No secret key...!")
            return None

        diariosdk = Diario(APP_ID, SECRET_KEY)
        response = diariosdk.get_pdf_info(document_hash)

        if not response.data:
            response = diariosdk.get_office_info(document_hash)
            if response.data:
                result = get_result(diariosdk, response.data)
        else:
            result = get_result(diariosdk, response.data)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        result = None

    return result
