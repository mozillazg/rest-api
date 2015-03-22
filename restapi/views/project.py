#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask import Blueprint, render_template, redirect, url_for, jsonify

from ..forms.project import ProjectForm
from ..models.api import Project

bp = Blueprint('projects', __name__)


@bp.route('/')
def projects():
    projects = Project.query.order_by(Project.updated_at.desc()).all()
    return render_template('project/index.html', projects=projects)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('.projects'))
    return render_template('project/create.html', form=form)


@bp.route('/<urlname>', methods=['DELETE'])
def view(urlname):
    project = Project.query.filter_by(urlname=urlname).first_or_404()
    project.delete()
    return jsonify(status='success')


@bp.route('/<urlname>/edit', methods=['GET', 'POST'])
def edit(urlname):
    project = Project.query.filter_by(urlname=urlname).first_or_404()
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        project.save()
        return redirect(url_for('.projects'))
    return render_template('project/edit.html', form=form, project=project)
