#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import os

from flask import Flask
from flask.ext.admin.contrib.sqla import ModelView

from .ext import admin, db, migrate
from .models.api import Project, Api


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder='templates',
    )
    app.config.from_pyfile('_config.py')

    if 'RESTAPI_CONFIG' in os.environ:
        app.config.from_envvar('RESTAPI_CONFIG')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.realpath(config))
    app.static_folder = app.config.get('STATIC_FOLDER')

    register_db_events(app)
    register_db(app)
    regisetr_admin(app)

    register_hooks(app)
    register_blueprints(app)
    register_logger(app)

    return app


def register_hooks(app):
    pass


def register_db(app):
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)


def register_db_events(app):
    pass


def regisetr_admin(app):
    MyModelView = type(str("MyModelView"), (ModelView,), {})
    MyModelView.column_display_pk = True
    MyModelView.column_default_sort = ('id', True)
    admin.add_view(MyModelView(Project, db.session))
    admin.add_view(MyModelView(Api, db.session))

    admin.init_app(app)


def create_db():
    db.create_all()


def register_blueprints(app):
    pass


def register_logger(app):
    """Track the logger for production mode."""
    if app.debug:
        return
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
