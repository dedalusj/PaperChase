# -*- coding: utf-8 -*-
"""
    keepupwithscience.api
    ~~~~~~~~~~~~~

    keepupwithscience api application package
"""

from functools import wraps

from .. import factory
import flask.ext.restless
from ..models import *


def create_app(settings_override=None, register_security_blueprint=False):
    """Returns the KeepUpWithScience API application instance"""

    app = factory.create_app(__name__, __path__, settings_override,
                             register_security_blueprint=register_security_blueprint)

    manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)	

    manager.create_api(Journal)
    manager.create_api(Category)
    manager.create_api(Paper)
    
    return app