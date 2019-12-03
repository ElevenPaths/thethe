#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
'''


class ExternalApiCompareRequest:

    FIELD_MATCHING_FIELDS = "matchingFields"
    FIELD_MATCHING_QUERY = "matchingQuery"
    FIELD_APPS = "apps"

    apps = []
    include_details = None

    def __init__(self, apps, include_details):
        self.apps = apps
        self.include_details = include_details

    def get_json_encode_for_compare_apps(self):
        json_data = dict()
        if self.apps is not None:
            json_data["apps"] = self.apps
        if self.include_details is not None:
            json_data["includeDetails"] = self.include_details

        return json_data