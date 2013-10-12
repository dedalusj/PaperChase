# -*- coding: utf-8 -*-
"""
    paperchase.api
    ~~~~~~~~~~~~~

    paperchase api application package
"""

from flask.ext.restful import Api

from .. import factory

from .journals import CategoryAPI, CategoryListAPI, SubcategoryListAPI, CategoryJournalsAPI, JournalListAPI, JournalAPI, SuggestionAPI
from .users import UserAPI, RegisterAPI
from .subscriptions import SubscriptionListAPI, SubscriptionAPI
from .papers import PaperListAPI, PaperAPI, UnreadPapersAPI, ReadPapersAPI, MarkAllPapersAPI

def create_app(settings_override=None):
    """
    Returns the paperchase API :class:`Flask` instance.
    
    :param settings_override: dictionary of settings to override
    """
    app = factory.create_app(__name__, __path__, settings_override)
    api = Api(app)
    
    # API endpoints connected to the Journal model
    api.add_resource(CategoryListAPI, '/categories')
    api.add_resource(CategoryAPI, '/categories/<int:id>')
    api.add_resource(SubcategoryListAPI, '/categories/<int:id>/subcategories')
    api.add_resource(CategoryJournalsAPI, '/categories/<int:id>/journals')
    api.add_resource(JournalListAPI, '/journals')
    api.add_resource(JournalAPI, '/journals/<int:id>')
    api.add_resource(SuggestionAPI, '/suggestion')
    
    # API endpoints connected to the User model
    api.add_resource(UserAPI, '/users')
    api.add_resource(RegisterAPI, '/register')
    api.add_resource(SubscriptionListAPI, '/subscriptions')
    api.add_resource(SubscriptionAPI, '/subscriptions/<int:id>')
    
    # API endpoints connected to the Paper model
    api.add_resource(PaperListAPI, '/papers')
    api.add_resource(PaperAPI, '/papers/<int:id>')
    api.add_resource(UnreadPapersAPI, '/unread_papers')
    api.add_resource(ReadPapersAPI, '/read_papers')
    api.add_resource(MarkAllPapersAPI, '/read_papers/mark_all_read')
    
    return app