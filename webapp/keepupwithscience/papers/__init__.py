# -*- coding: utf-8 -*-
"""
    keepupwithscience.papers
    ~~~~~~~~~~~~~~~~~

    keepupwithscience papers package
"""

from ..core import Service
from .models import Paper

class PapersService(Service):
    __model__ = Paper
