import json
from django.conf import settings
from rest_framework.response import Response

VERSION="1.0.0"
settings.CONTENT_TYPE = "application/json;charset=utf8"


class MakeJSON(object):
    """initialize dictionary"""
    def __init__(self):
        self.header = dict()
        self.result = dict()
        self.total = dict()

    def __del__(self):
        pass

    """make header dictionary"""
    def setHeader(self, version, code, message):
        self.header['version'] = VERSION
        self.header['code'] = int(code)
        self.header['message'] = message

    """add result dictionary"""
    def addResult(self, **kwargs):
        for name, value in kwargs.items():
            self.result[name] = value

    """return Json"""
    def getJson(self):
        self.total['header'] = self.header
        self.total['result'] = self.result
        if 'code' not in self.total['result']:
            self.total['result']['code'] = 999

        context = self.total

        return context

    def get500Response(self):
        self.header['version'] = VERSION
        self.header['code'] = 500
        self.header['message'] = "Server Error occured"
        self.total['header'] = self.header
        self.total['result'] = self.result
        if 'code' not in self.total['result']:
            self.total['result']['code'] = 999

        return self.total

    def get400Response(self):
        self.header['version'] = VERSION
        self.header['code'] = 400
        self.header['message'] = "Ruined Request"
        self.total['header'] = self.header
        self.total['result'] = self.result
        if 'code' not in self.total['result']:
            self.total['result']['code'] = -1

        return self.total

    def get404Response(self):
        self.header['version'] = VERSION
        self.header['code'] = 404
        self.header['message'] = "Ruined Request"
        self.total['header'] = self.header
        self.total['result'] = self.result
        if 'code' not in self.total['result']:
            self.total['result']['code'] = -1

        return self.total

    def get200Response(self, code, explain):
        self.total['header'] = self.header
        self.result['code'] = code
        self.result['explain'] = explain
        self.total['result'] = self.result
        if 'code' not in self.total['result']:
            self.total['result']['code'] = 999

        return self.total

    def getResponse(self):
        return Response(self.getJson(), content_type=settings.CONTENT_TYPE)

    def get400ResponseWithResponse(self):
        return Response(self.get400Response(), content_type=settings.CONTENT_TYPE)

    def clean(self):
        self.header = dict()
        self.result = dict()
        self.total = dict()
