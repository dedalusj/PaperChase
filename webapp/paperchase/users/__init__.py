# -*- coding: utf-8 -*-
"""
    paperchase.users
    ~~~~~~~~~~~~~~

    paperchase users package
"""
from flask import request

from ..core import Service
from .models import User, subscriptions_users


class UsersService(Service):
    __model__ = User

    def get_pw(self, username):
        """Flask-HTTPAuth method to validate a Basic HTTP Authentication."""
        user = self.first(email=username)
        if user:
            return user.password
        return None

    def request_user(self):
        """
        Return the :class:`User` corresponding to the username passed
        in the HTTP request.

        By the tyme this method is called we are past the authentication
        stage of the API hence we are ensured a user with such email exists
        """
        return self.first(email=request.authorization.username)

    def is_subscribed(self, user, journal):
        return user.subscriptions.filter(
            subscriptions_users.c.journal_id == journal.id).count() > 0

    def subscribe(self, user, journal):
        if not self.is_subscribed(user, journal):
            user.subscriptions.append(journal)
            self.save(user)
            return user

    def unsubscribe(self, user, journal):
        if self.is_subscribed(user, journal):
            user.subscriptions.remove(journal)
            self.save(user)
            return user
