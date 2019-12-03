#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

from sdklib.http import HttpSdk
from sdklib.http.authorization import X11PathsAuthentication
from sdklib.http.renderers import MultiPartRenderer

from tasks.deps.tacyt.ExternalApiFilterRequest import ExternalApiFilterRequest
from tasks.deps.tacyt.ExternalApiTagRequest import ExternalApiTagRequest
from tasks.deps.tacyt.Filter import Filter
from tasks.deps.tacyt.ExternalApiCompareRequest import ExternalApiCompareRequest
from tasks.deps.tacyt.ExternalApiSearchRequest import ExternalApiSearchRequest
from tasks.deps.tacyt.ExternalApiEngineVersionRequest import (
    ExternalApiEngineVersionRequest,
)
from tasks.deps.tacyt.Version import Version
import urllib3
import json

json_encode = lambda x: json.dumps(x)
json_decode = lambda x: json.loads(x)

PORT = 443
HOST = "https://tacyt.elevenpaths.com/"


...
urllib3.disable_warnings()


class TacytApp(HttpSdk):
    API_SEARCH_URL = "/api/" + Version.API_VERSION + "/search"
    API_DETAILS_URL = "/api/" + Version.API_VERSION + "/details"
    API_FILTERS_URL = "/api/" + Version.API_VERSION + "/filters"
    API_TAGS_URL = "/api/" + Version.API_VERSION + "/tags"
    API_COMPARER_URL = "/api/" + Version.API_VERSION + "/compare"
    API_UPLOAD_URL = "/api/" + Version.API_VERSION + "/upload"
    API_ENGINE_VERSION_URL = "/api/" + Version.API_VERSION + "/engineVersion"

    def __init__(self, app_id, secret_key, host=HOST, port=PORT):
        """Initialize the DIARIO SDK with provided user information.
        :param app_id: User appId to be used
        :param secret_key: User secretKey to be used
        :param host: IP address or domain
        :param port: TCP port
        """
        HOST = "{0}:{1}".format(host, port)
        super(TacytApp, self).__init__(host=HOST)

        self.app_id = app_id
        self.secret_key = secret_key
        self.authentication_instances += (
            X11PathsAuthentication(self.app_id, self.secret_key),
        )

    def search_apps(
        self, query, number_page=None, max_results=None, outfields=None, grouped=None
    ):
        """
        @param $query The query string will filter the search results.
        @param $numberPage A number greater or equal to 1 indicating the page of results which have to be retrieved.
        @param $maxResults A number between 1 and 100 indicating the max number of apps which have to be retrieved.
        @return Json structure with the keys to the Applications found.
        """
        result = ExternalApiSearchRequest(
            query, number_page, max_results, outfields, grouped
        )
        print(result.get_json_encode_for_search())
        return self.post(
            url_path=self.API_SEARCH_URL,
            body_params=result.get_json_encode_for_search(),
        )

    def get_app_details(self, key):
        """
        @param $key The key of an application.
        @return Json structure with the details of an application.
        """
        return self.get(url_path=self.API_DETAILS_URL + "/" + key)

    def list_tags(self):
        """
        @return A list of tags that have been created.
        """
        result = ExternalApiTagRequest(ExternalApiTagRequest.LIST_REQUEST, None, None)
        return self.post(
            url_path=self.API_TAGS_URL,
            body_params=result.get_json_encode_dict_for_tag_based_requests(),
        )

    def assign_tag(self, tag, app_keys):
        """
        This method associates a tag created with applications.
        @param $tag the name of the tag to create
        @param $app_keys Key applications that want to associate with the tag
        @return A list of applications associates with a tag.
        """
        result = ExternalApiTagRequest(
            ExternalApiTagRequest.CREATE_REQUEST, tag, app_keys
        )
        return self.post(
            url_path=self.API_TAGS_URL,
            body_params=result.get_json_encode_dict_for_tag_based_requests(),
        )

    def remove_tag_for_apps(self, tag, app_keys):
        """
        This method remove a tag associate with applications.
        @param $tag the name of the tag to create
        @param $app_keys Key applications that want to remove with the tag
        """
        result = ExternalApiTagRequest(
            ExternalApiTagRequest.REMOVE_REQUEST, tag, app_keys
        )
        return self.post(
            url_path=self.API_TAGS_URL,
            body_params=result.get_json_encode_dict_for_tag_based_requests(),
        )

    def delete_tag(self, tag):
        """
        This method delete a tag.
        @param $tag the name of the tag you want to delete.
        """
        result = ExternalApiTagRequest(
            ExternalApiTagRequest.REMOVE_ALL_REQUEST, tag, None
        )
        return self.post(
            url_path=self.API_TAGS_URL,
            body_params=result.get_json_encode_dict_for_tag_based_requests(),
        )

    def create_filter(self, filter):
        """
        This method create a filter.
        @param $filter Filter structure.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.CREATE_REQUEST, filter, 0, None
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_for_filter_based_requests(),
        )

    def update_filter(self, filter):
        """
        This method update changes associates with a filter.
        @param $filter Filter structure.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.UPDATE_REQUEST, filter, 0, None
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_for_filter_based_requests(),
        )

    def read_group_filters(self):
        """
        @return all group filters created
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.READ_GROUPS, None, 0, None
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_for_filter_based_requests(),
        )

    def read_all_filters(self):
        """
        @return a list of filters creates.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.READ_REQUEST, None, 0, None
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_for_filter_based_requests(),
        )

    def read_one_filter(self, filter_id):
        """
        @param $filter_id id of the filter you want to read.
        @return This method returns the details of filter associate with this filter_id.
        """
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.READ_REQUEST, filter, 0, None
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_for_filter_based_requests(),
        )

    def delete_filter(self, filter_id):
        """
     	This method delete a filter create.
        @param $filter_id id of the filter you want to delete.
        """
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.DELETE_REQUEST, filter, 0, None
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_for_filter_based_requests(),
        )

    def search_public_filter(self, query, page):
        """
        @param $query any word or phrase within the description or title Filter
        @param $page A number greater or equal to 1 indicating the page of results which have to be retrieved.
        @return A list of public filters(Visibility = Public)
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.SEARCH_PUBLIC_FILTER_REQUEST, None, page, query
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_dict_filter_for_content_based_requests(),
        )

    def list_detected_apps(self, page, filter_id):
        """
        @param $filter_id id to the filter.
        @return Json structure with the details of applications detected by the filter.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.LIST_DETECTIONS_REQUEST, None, page, filter_id
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_dict_filter_for_content_based_requests(),
        )

    def list_group_detected_apps(self, page, groupName):
        """
        @param $groupName name of the group.
        @param $page A number greater or equal to 1 indicating the page of results which have to be retrieved.
        @return Json structure with the details of applications detected by the filters group.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.LIST_GROUP_DETECTIONS, None, page, groupName
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_dict_filter_for_content_based_requests(),
        )

    def unsubscribe_public_filter(self, filter_id):
        """
        With this method you can subscribe to filter.
        @param $filter_id id to filter you want subscribe.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.UNSUBSCRIBE_REQUEST, None, 0, filter_id
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_dict_filter_for_content_based_requests(),
        )

    def subscribe_public_filter(self, filter_id):
        """
        With this method you can unsubscribe to filter.
        @param $filter_id id to filter you want unsubscribe.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.SUBSCRIBE_REQUEST, None, 0, filter_id
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_dict_filter_for_content_based_requests(),
        )

    def get_RSS_info(self, filter_id):
        """
        This method get the RSS information of a filter.
        @param $filter_id id to filter you want get RSS information.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.GET_RSS_REQUEST, None, None, filter_id
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_dict_filter_for_content_based_requests(),
        )

    def get_group_RSS_info(self, groupName):
        """
        This method get the RSS information of a filters group.
        @param $groupName name of the filters group you want get RSS information.
        """
        result = ExternalApiFilterRequest(
            ExternalApiFilterRequest.GET_GROUP_RSS, None, None, groupName
        )
        return self.post(
            url_path=self.API_FILTERS_URL,
            body_params=result.get_json_encode_dict_filter_for_content_based_requests(),
        )

    def compare_apps(self, apps, include_details):
        """
        @param $apps the key of the app you want to compare. The array of apps is limited to 10 apps.
        @param $include_details with a value of true in includeDetails you will get not only the matching fields and their values, but all the values defined for the applications.
        """
        result = ExternalApiCompareRequest(apps, include_details)
        return self.post(
            url_path=self.API_COMPARER_URL,
            body_params=result.get_json_encode_for_compare_apps(),
        )

    def upload_app(self, apk_file, tag_name=None):
        """
        Upload app to Tacyt
        :param tag_name: put tag and apk
        :param apk_file: path to file apk
        :return: Response
        """
        try:

            file_content = open(apk_file, "rb").read()
            file_name = uuid.uuid4().hex
            return self.post(
                url_path=self.API_UPLOAD_URL,
                files={"file": (file_name, file_content)},
                renderers=MultiPartRenderer(),
                body_params={"tagName": tag_name},
            )

        except Exception as e:
            print(repr(e))
            return None

    def get_engine_version(self, date=None, engine_id=None, lang=None):
        """
        Search an engine and its associated vulnerabilities. If no params return a list of all existing engines
        :param engine_id: engine id.
        :param date: search the engine available on that date.
        :param lang: output language of vulnerabilities fields. Values "es" or "en".
        :return: Response
        """
        params = ""
        if engine_id or date or lang:
            external_engine_version = ExternalApiEngineVersionRequest(
                date, engine_id, lang
            )
            params = "?" + external_engine_version.get_encoded_params()
        return self.get(url_path=self.API_ENGINE_VERSION_URL, query_params=params)
