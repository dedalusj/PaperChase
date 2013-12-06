# -*- coding: utf-8 -*-
"""
    paperchase.journals
    ~~~~~~~~~~~~~~~

    paperchase journals package
"""
from sqlalchemy import or_

from ..core import Service
from .models import Journal, Category, Path, journals_categories


class CategoryService(Service):
    __model__ = Category

    def all_journals(self, category):
        """
        Return all the journals for a given category even the journals
        of its parent.
        """
        return Journal.query.join(journals_categories,(journals_categories.c.journal_id == Journal.id)).filter(or_(journals_categories.c.category_id == category.id, journals_categories.c.category_id == category.parent_id))


class JournalsService(Service):
    __model__ = Journal

    def __init__(self, *args, **kwargs):
        super(JournalsService, self).__init__(*args, **kwargs)
        self.categories = CategoryService()

    def _preprocess_params(self, kwargs):
        kwargs = super(JournalsService, self)._preprocess_params(kwargs)
        categories = kwargs.get('categories', [])
        if categories and all(isinstance(c, int) for c in categories):
            kwargs['categories'] = self.categories.get_all(*categories)
        return kwargs

    def all(self, user=None):

        """
        Retrieve all the journals in the database. If a user is provided it appends a
        `subscribed` flag attribute to every journal to mark the user subscriptions.
        """

        if user is None:
            return super(JournalsService, self).all()
        journals = self.__model__.query.order_by(self.__model__.id).all()
        subscriptions = user.subscriptions.order_by(self.__model__.id).all()
        sub_index = 0
        for journal in journals:
            if sub_index >= len(subscriptions) or journal.id < subscriptions[sub_index].id:
                journal.subscribed = False
            else:
                journal.subscribed = True
                sub_index += 1
        return journals


class PathService(Service):
    __model__ = Path
