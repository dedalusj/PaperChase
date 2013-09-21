# -*- coding: utf-8 -*-
"""
    paperchase.api
    ~~~~~~~~~~~~~

    paperchase api application package
"""

from functools import wraps

from .. import factory
from flask.ext.restful import Api
from .journals import CategoryAPI, CategoryListAPI, SubcategoryListAPI, CategoryJournalsAPI, JournalListAPI, JournalAPI, SuggestionAPI
from .users import UserAPI

def create_app(settings_override=None):
    """Returns the paperchase API application instance"""

    app = factory.create_app(__name__, __path__, settings_override, register_security_blueprint=False)
    api = Api(app)
    
    api.add_resource(CategoryListAPI, '/categories', endpoint = 'categories')
    api.add_resource(CategoryAPI, '/categories/<int:id>', endpoint = 'category')
    api.add_resource(SubcategoryListAPI, '/categories/<int:id>/subcategories', endpoint = 'subcategories')
    api.add_resource(CategoryJournalsAPI, '/categories/<int:id>/journals', endpoint = 'categoryJournal')
    api.add_resource(JournalListAPI, '/journals', endpoint = 'journals')
    api.add_resource(JournalAPI, '/journals/<int:id>', endpoint = 'journal')
    
    api.add_resource(SuggestionAPI, '/suggestion')
    
    api.add_resource(UserAPI, '/users/<string:email>')
    
    return app