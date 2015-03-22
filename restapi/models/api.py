#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from sqlalchemy.dialects.postgresql import JSON

from ._base import db, SessionMixin


class Project(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    urlname = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    def __init__(self, title=None, urlname=None, description=None):
        self.title = title
        self.urlname = urlname
        self.description = description

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Project {0}>'.format(self.title)


class Api(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship(
        'Project', backref=db.backref('apis', lazy='dynamic')
    )

    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    verb = db.Column(db.String(7), default='GET', doc='HTTP Method')
    arguments = db.Column(JSON)
    status_code = db.Column(db.Integer, default=200)
    headers = db.Column(JSON)
    body = db.Column(JSON)

    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    def __init__(self, title=None, url=None, verb='GET', status_code=200,
                 arguments=None, headers=None, body=None, description=None):
        self.title = title
        self.url = url
        self.verb = verb
        self.status_code = status_code
        self.arguments = arguments
        self.headers = headers
        self.body = body
        self.description = description

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<API {0}>'.format(self.title)
