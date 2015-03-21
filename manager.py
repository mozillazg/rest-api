#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server

from restapi.app import create_app

config = os.path.realpath('./etc/config.py')
if not os.path.exists(config):
    config = os.path.abspath('./etc/dev_config.py')

if 'RESTAPI_CONFIG' not in os.environ and os.path.exists(config):
    os.environ['RESTAPI_CONFIG'] = config

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Create database"""
    from restapi.app import create_db
    create_db()

if __name__ == '__main__':
    manager.run()
