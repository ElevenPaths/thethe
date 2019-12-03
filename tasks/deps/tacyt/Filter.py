
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 This library offers an API to use Tacyt in a python environment.
 Copyright (C) 2015 Eleven Paths
'''

class Filter():

    class Rule():

        weight = None
        content = None

        def __init__(self, weight=None, content=None):
            self.weight = weight
            self.content = content

        def get_json_encode(self):
            return {"weight": self.weight, "content": self.content}

    PUBLIC_VISIBILITY = "PUBLIC"
    PRIVATE_VISIBILITY = "PRIVATE"

    id = None
    name = None
    description = None
    weight = None
    visibility = PRIVATE_VISIBILITY
    rules = [Rule(None, None)]
    groups = None

    def __init__(self, id=None, name=None, description=None, weight=None, visibility=None, rules=None, groups=None):
        self.id = id
        self.name = name
        self.description = description
        self.weight = weight
        self.visibility = visibility
        self.rules = rules
        self.groups = groups

    def get_json_encode(self):

        result = {"id": self.id,
                  "name": self.name,
                  "description": self.description,
                  "weight": self.weight,
                  "visibility": self.visibility,
                  "rules": self.rules,
                  "groups": self.groups}

        filter_rules = list()

        if self.rules is not None:
            for rule in self.rules:
                filter_rules.append(rule.get_json_encode())

            result["rules"] = filter_rules

        return result