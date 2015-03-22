#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, abort

from ..forms.project import ApiForm
from ..models.api import Api, Project

bp = Blueprint('custom_api', __name__)


def check_urlname(func):
    @wraps
    def _wraper(urlname, *args, **kwargs):
        if not Project.query.filter_by(urlname=urlname).count():
            abort(404)
        return func(urlname, *args, **kwargs)
    return _wraper


@bp.route('/')
@check_urlname
def api_list(urlname):
    api_list = Api.query.order_by(Api.updated_at.desc()).all()
    return render_template('custom_api/index.html', api_list=api_list,
                           urlname=urlname)


@bp.route('/create', methods=['GET', 'POST'])
@check_urlname
def create(urlname):
    form = ApiForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('.api_list', urlname=urlname))
    return render_template('custom_api/create.html', form=form)


@bp.route('/<pk>')
@check_urlname
def view(urlname, pk):
    api = Api.query.filter_by(id=pk).first_or_404()
    return render_template('custom_api/view.html', api=api)


@bp.route('/<pk>/edit', methods=['GET', 'POST'])
@check_urlname
def edit(urlname, pk):
    api = Api.query.filter_by(id=pk).first_or_404()
    form = ApiForm(obj=api)
    if form.validate_on_submit():
        form.populate_obj(api)
        api.save()
        return redirect(url_for('.api_list', urlname=urlname))
    return render_template('custom_api/edit.html', form=form, api=api)
