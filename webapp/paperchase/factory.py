# -*- coding: utf-8 -*-
"""
    paperchase.factory
    ~~~~~~~~~~~~~~~~

    paperchase factory module
"""

import os
from celery import Celery
from flask import Flask
from flask.ext.seasurf import SeaSurf

from .core import db, mail
from .helpers import register_blueprints

def create_app(package_name, package_path, settings_override=None):
    """
    Returns a :class:`Flask` application instance configured with common
    functionality for the paperchase platform.
    
    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    """
    app = Flask(package_name, instance_relative_config=True)
        
    app.config.from_object('paperchase.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    if settings_override is not None:
        app.config.update(settings_override)
    
    db.init_app(app)
    mail.init_app(app)
    csrf = SeaSurf(app)
	
    register_blueprints(app, package_name, package_path)

    return app

def create_celery_app(app=None):
    """
    Returns a :class:`Celery` instance configured from the config dictionary
    of the app.
    
    :param app: application
    """
    app = app or create_app('paperchase', os.path.dirname(__file__))
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery