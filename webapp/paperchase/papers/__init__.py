# -*- coding: utf-8 -*-
"""
    paperchase.papers
    ~~~~~~~~~~~~~~~~~

    paperchase papers package
"""

from ..core import Service
from .models import Paper, UserPaper

class PapersService(Service):
    __model__ = Paper
    
class UserPapersService(Service):
    __model__ = UserPaper
