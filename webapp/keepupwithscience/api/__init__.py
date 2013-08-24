# -*- coding: utf-8 -*-
"""
    keepupwithscience.api
    ~~~~~~~~~~~~~

    keepupwithscience api application package
"""

from functools import wraps

from .. import factory
from flask.ext.restful import Api
from .categories import CategoryAPI, CategoryListAPI

def create_app(settings_override=None):
    """Returns the KeepUpWithScience API application instance"""

    app = factory.create_app(__name__, __path__, settings_override, register_security_blueprint=False)
    api = Api(app)
    
    api.add_resource(CategoryListAPI, '/categories', endpoint = 'categories')
    api.add_resource(CategoryAPI, '/categories/<int:id>', endpoint = 'category')
    
    return app