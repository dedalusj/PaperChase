# -*- coding: utf-8 -*-
"""
    keepupwithscience.journals
    ~~~~~~~~~~~~~~~

    keepupwithscience journals package
"""

from ..core import Service, KeepUpWithScienceError
from .models import Journal, Category

class CategoryService(Service):
    __model__ = Category

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
    