#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired

from ..models.api import Project, Api
from ._base import BaseForm


class ProjectForm(BaseForm):
    title = StringField('Title', validators=[DataRequired()])
    urlname = StringField('URLName', validators=[DataRequired()])
    description = TextAreaField('Description')

    def validate_urlname(self, field):
        if self._obj and self._obj.urlname == field.data:
            return
        if Project.query.filter_by(urlname=field.data).scalar():
            raise ValueError('The project exists')

    def save(self):
        project = Project(**self.data)
        project.save()
        return project


class ApiForm(BaseForm):
    title = StringField('title', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired()])
    verb = StringField('verb', validators=[DataRequired()])
    status_code = IntegerField('status_code', validators=[DataRequired()])
    arguments = TextAreaField('arguments')
    headers = TextAreaField('headers')
    body = TextAreaField('body')
    description = TextAreaField('description')

    def save(self):
        api = Api(**self.data)
        api.save()
        return api
