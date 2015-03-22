#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

DEBUG = False
TESTING = False

SECRET_KEY = 'your secret key'

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    os.getcwd(), 'db.sqlite'
)
STATIC_FOLDER = os.path.join(ROOT_DIR, 'static')
