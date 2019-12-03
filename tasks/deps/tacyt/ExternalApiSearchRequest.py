#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
'''

from io import StringIO


class ExternalApiSearchRequest:
    grouped = None
    numberPage = 1
    maxResults = 20
    query = None
    outputFields = None

    def __init__(self, query=None, numberPage=None, maxResults=None, outputFields=None, grouped=None):

        string_build = StringIO()
        if numberPage and numberPage <= 0:
            self.numberPage = 1
        else:
            self.numberPage = numberPage

        if numberPage and maxResults <= 0:
            self.maxResults = 20

        else:
            self.maxResults = maxResults

        if outputFields != None and len(outputFields) > 0:
            for field in outputFields:
                string_build.write(field + ",")

        self.outputFields = string_build.getvalue()
        self.grouped = grouped
        self.query = query

    def get_json_encode_for_search(self):

        json_data = dict()
        if self.query is not None:
            json_data["query"] = self.query
        if self.numberPage is not None:
            json_data["numberPage"] = self.numberPage
        if self.maxResults is not None:
            json_data["maxResults"] = self.maxResults
        if self.outputFields is not None:
            json_data["outputFields"] = self.outputFields
        if self.grouped is not None:
            json_data["grouped"] = self.grouped

        return json_data
