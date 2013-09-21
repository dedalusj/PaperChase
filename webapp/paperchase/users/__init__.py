# -*- coding: utf-8 -*-
"""
    paperchase.users
    ~~~~~~~~~~~~~~

    paperchase users package
"""

from ..core import Service
from .models import User

class UsersService(Service):
    __model__ = User