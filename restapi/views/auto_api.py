#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask import Blueprint
from flask.ext.restful import abort, Api, reqparse, Resource

from ..models.api import Project, Api as ApiModel
from ..ext import db

bp = Blueprint('auto_api', __name__)
api = Api(bp, catch_all_404s=True)


class API(Resource):

    def get(self, path):
        return {'path': path}

    def head(self, path):
        pass

    def post(self, path):
        pass

    def patch(self, path):
        pass

    def put(self, path):
        pass

    def delete(self, path):
        pass

    def options(self, path):
        pass

api.add_resource(API, '<path:path>')
