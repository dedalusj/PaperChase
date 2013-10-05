# -*- coding: utf-8 -*-
"""
    paperchase.users
    ~~~~~~~~~~~~~~

    paperchase users package
"""
from flask import request

from ..core import Service
from .models import User

class UsersService(Service):
    __model__ = User
    
    def get_pw(self,username):
        """Flask-HTTPAuth method to validate a Basic HTTP Authentication."""
        user = self.first(email = username)
        if user:
            return user.password
        return None
    
    def request_user(self):
        """
        Return the :class:`User` corresponding to the username passed
        in the HTTP request.
        """
        return self.first(email = request.authorization.username)