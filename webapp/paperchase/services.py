# -*- coding: utf-8 -*-
"""
    paperchase.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .papers import PapersService, UserPapersService
from .journals import JournalsService, CategoryService, PathService
from .users import UsersService

#: An instance of the :class:`PapersService` class
papers = PapersService()

#: An instance of the :class:`UserPapersService` class
user_papers = UserPapersService()

#: An instance of the :class:`JournalsService` class
journals = JournalsService()

#: An instance of the :class:`CategorysService` class
categories = CategoryService()

#: An instance of the :class:`PathService` class
paths = PathService()

#: An instance of the :class:`UsersService` class
users = UsersService()