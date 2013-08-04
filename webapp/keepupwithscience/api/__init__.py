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
from ..helpers import http_auth_func

def create_app(settings_override=None):
    """Returns the KeepUpWithScience API application instance"""

    app = factory.create_app(__name__, __path__, settings_override, register_security_blueprint=False)

    manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)	

    common_configurations = dict(preprocessors=dict(GET_SINGLE=[http_auth_func],GET_MANY=[http_auth_func]), url_prefix=None)

    manager.create_api(Journal, include_columns=['id', 'url', 'title', 'short_title', 'last_checked', 'categories', 'categories.id', 'categories.name'], **common_configurations)
    manager.create_api(Category, include_columns=['id', 'name', 'description', 'journals', 'journals.id', 'journals.title', 'journals.url', 'journals.short_title', 'journals.last_checked'], **common_configurations)
    manager.create_api(Paper, results_per_page=50, include_columns=['id', 'title', 'abstract', 'authors', 'url', 'doi', 'journal', 'journal.title'], **common_configurations)
    
    return app