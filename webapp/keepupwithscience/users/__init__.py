# -*- coding: utf-8 -*-
"""
    keepupwithscience.users
    ~~~~~~~~~~~~~~

    keepupwithscience users package
"""

from ..core import Service
from .models import User

class UsersService(Service):
    __model__ = User