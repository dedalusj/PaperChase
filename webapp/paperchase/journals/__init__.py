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
        """Return all the journals for a given category even the journals of its parent."""
        return Journal.query.join(journals_categories, (journals_categories.c.journal_id == Journal.id)).filter(or_(journals_categories.c.category_id == category.id, journals_categories.c.category_id == category.parent_id))

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
    
class PathService(Service):
    __model__ = Path