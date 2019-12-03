#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
'''
try:
    import simplejson as json

except ImportError:
    import json

json_encode = lambda x: json.dumps(x)
json_decode = lambda x: json.loads(x)

class ExternalApiTagRequest:

    LIST_REQUEST = "LIST"
    CREATE_REQUEST = "CREATE"
    REMOVE_REQUEST = "REMOVE"
    REMOVE_ALL_REQUEST = "REMOVE_ALL"

    request_type = None
    tag = None
    apps = []

    def __init__(self, request_type=None, tag=None, apps=None):
        self.request_type = request_type
        self.tag = tag
        self.apps = apps

    def get_json_encode_dict_for_tag_based_requests(self):
        json_obj = dict()
        if self.request_type is not None:
            json_obj["requestType"] = self.request_type
        if self.tag is not None:
            json_obj["tag"] = self.tag
        if self.apps is not None:
            json_obj["apps"] = self.apps

        return json_obj

    def get_json_encode_string(self):

        return json_encode(self.get_json_encode_dict_for_tag_based_requests())
