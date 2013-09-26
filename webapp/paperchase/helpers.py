# -*- coding: utf-8 -*-
"""
    paperchase.helpers
    ~~~~~~~~~~~~~~~~

    paperchase helpers module
"""

import pkgutil
import importlib
from datetime import timedelta
import feedparser
from flask import Blueprint, request

from .core import auth
from .services import users

@auth.get_password
def get_pw(username):
    user = users.first(email = username)
    if user:
        return user.password
    return None

def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv
        
def days_since(t1, t2):
        """
        Returns the number of days between the two timestamps.

        :param t1 Time one.
        :param t2 Time two.
        """
        timedelta = t1 - t2
        return timedelta.days

def deltatime(period, frequency):
    frequency = int(frequency)
    if period == 'hourly':
        return timedelta(hours=1/frequency)
    elif period == 'daily':
        return timedelta(days=1/frequency)
    elif period == 'weekly':
        return timedelta(weeks=1/frequency)
    elif period == 'monthly':
        return timedelta(days=30/frequency)
    elif period == 'yearly':
        return timedelta(days=365/frequency)
    return None
    
def bozo_checker(bozo_exception):
    """
    This function checks if the bozo exception is a critical exception or
    a exception that can be ignored.

    :param bozo_exception The bozo exception to test.
    """
    # Will return false by default, so only whitelisted exceptions will
    # return true.
    return_val = False

    # This exception is raised when the feed was decoded and parsed using a different encoding than what the server/feed
    # itself claimed it to be.
    if isinstance(bozo_exception, feedparser.CharacterEncodingOverride):
        return_val = True

    return return_val