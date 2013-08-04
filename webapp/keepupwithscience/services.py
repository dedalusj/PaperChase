# -*- coding: utf-8 -*-
"""
    keepupwithscience.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .papers import PapersService
from .journals import JournalsService, CategoryService
from .users import UsersService

#: An instance of the :class:`PapersService` class
papers = PapersService()

#: An instance of the :class:`JournalsService` class
journals = JournalsService()

#: An instance of the :class:`CategoriesService` class
categories = CategoryService()

#: An instance of the :class:`UsersService` class
users = UsersService()