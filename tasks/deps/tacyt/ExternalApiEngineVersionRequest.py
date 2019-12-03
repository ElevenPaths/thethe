#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

class ExternalApiEngineVersionRequest:

    def __init__(self, date, engineId,  lang):
        self.params = [("date", date), ("engineId", engineId), ("lang", lang)]

    def get_encoded_params(self):

        paramsNotNone = [(name, value) for name, value in self.params if value is not None]
        paramsEncoded = urllib.urlencode(paramsNotNone)

        return paramsEncoded