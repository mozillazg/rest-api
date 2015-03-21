#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask import current_app
from flask.ext.admin import Admin
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.local import LocalProxy

admin = Admin(name='rest-api admin')
db = SQLAlchemy()
migrate = Migrate()


def get_logger():
    return current_app.logger
logger = LocalProxy(get_logger)
