#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from functools import wraps

from flask import Blueprint, request
from flask.ext.restful import abort, Api, reqparse, Resource

from ..ext import logger
from ..models.api import Project

bp = Blueprint('auto_api', __name__)
api = Api(bp, catch_all_404s=True)


def check_url(func):
    @wraps(func)
    def wrapper(path):
        logger.debug(path)
        # check url_prefix
        url_prefix = path.strip('/').split('/')[0]
        logger.debug(url_prefix)
        projects = Project.query.filter_by(urlname=url_prefix)
        if not projects.scalar():
            abort(404)

        project = projects.first()
        # check api RUL
        api_url = path.lstrip('/').lstrip(url_prefix)
        logger.debug(api_url)
        apis = project.apis.filter_by(url=api_url)
        if not apis.scalar():
            abort(404)

        # check HTTP Method
        verb = request.method
        logger.debug(verb)
        api_obj = apis.filter_by(verb=verb).first()
        if not api_obj:
            # if verb == 'OPTIONS':
            #     # verbs = set([x.verb for x in apis] + ['OPTIONS'])
            #     # return '', 200, {'Allow': ', '.join(verbs)}
            # else:
            abort(405)

        return func(path, api_obj)

    return wrapper


def handle_request(func):
    @wraps(func)
    def wrapper(self, path, api_obj):
        if api_obj.arguments:
            gen_reqparse(api_obj.arguments).parse_args()
        return api_obj.body, api_obj.status_code, api_obj.headers or {}

    return wrapper


def gen_reqparse(arguments):
    req = reqparse.RequestParser()
    for arg in arguments:
        _type = {
            'int': int,
            'float': float,
            'string': unicode,
        }.get(arg['type'], str)
        req.add_argument(
            arg['name'], type=_type, required=arg['required'],
            location='json'
        )

    return req


class API(Resource):
    method_decorators = [check_url]

    @handle_request
    def get(self, path, api_obj):
        return {'path': path}

    @handle_request
    def head(self, path, api_obj):
        pass

    @handle_request
    def post(self, path, api_obj):
        pass

    @handle_request
    def patch(self, path, api_obj):
        pass

    @handle_request
    def put(self, path, api_obj):
        pass

    @handle_request
    def delete(self, path, api_obj):
        pass

    @handle_request
    def options(self, path, api_obj):
        pass

api.add_resource(API, '<path:path>')
