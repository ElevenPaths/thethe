import traceback
import json
import requests

from diario import Diario

from tasks.api_keys import KeyRing

APP_ID = KeyRing().get("diario-appid")
SECRET_KEY = KeyRing().get("diario-secret")

__PREDICTION = {"M": "Malware", "G": "Goodware", "NM": "No macros"}
__STATUS = {"A": "Analyzed", "P": "Processing", "F": "Failed"}


def diario(document_hash):
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
