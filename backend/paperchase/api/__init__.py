# -*- coding: utf-8 -*-
"""
    paperchase.api
    ~~~~~~~~~~~~~

    paperchase api application package
"""

from flask.ext.restful import Api

from .. import factory

from .journals import CategoryAPI, CategoryListAPI, JournalListAPI, JournalAPI, SuggestionAPI
# SubcategoryListAPI, CategoryJournalsAPI
from .users import UserAPI, RegisterAPI, UserToken
from .subscriptions import SubscriptionListAPI, SubscriptionAPI
from .papers import PaperListAPI, PaperAPI, UnreadPapersAPI,\
    ReadPapersAPI, MarkAllPapersAPI


def create_app(settings_override=None):
    """
    Returns the paperchase API :class:`Flask` instance.

    :param settings_override: dictionary of settings to override
    """
    app = factory.create_app(__name__, __path__, settings_override)
    api = Api(app)

    # API endpoints connected to the Journal model
    api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
    api.add_resource(CategoryAPI, '/categories/<int:id>', endpoint='category')
    api.add_resource(JournalListAPI, '/journals', endpoint='journals')
    api.add_resource(JournalAPI, '/journals/<int:id>', endpoint='journal')
    api.add_resource(SuggestionAPI, '/suggestion', endpoint='suggestion')

    # API endpoints connected to the User model
    api.add_resource(UserAPI, '/users', endpoint='users')
    api.add_resource(UserToken, '/users/token', endpoint='token')
    api.add_resource(RegisterAPI, '/register', endpoint='register')
    api.add_resource(SubscriptionListAPI, '/subscriptions', endpoint='subscriptions')
    api.add_resource(SubscriptionAPI, '/subscriptions/<int:id>', endpoint='subscription')

    # API endpoints connected to the Paper model
    api.add_resource(PaperListAPI, '/papers', '/journals/<int:journal_id>/papers',
                     endpoint='papers')
    api.add_resource(PaperAPI, '/papers/<int:id>', endpoint='paper')
    api.add_resource(UnreadPapersAPI, '/unread_papers', endpoint='unread_papers')
    api.add_resource(ReadPapersAPI, '/read_papers', endpoint='read_papers')
    api.add_resource(MarkAllPapersAPI, '/read_papers/mark_all_read', endpoint='mark_all_read')

    return app
