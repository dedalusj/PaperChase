# -*- coding: utf-8 -*-
"""
    keepupwithscience.helpers
    ~~~~~~~~~~~~~~~~

    keepupwithscience helpers module
"""

import pkgutil
import importlib

from flask import Blueprint, request
from flask.ext.restless import ProcessingException
from flask_security.utils import verify_and_update_password

from .services import users

def http_auth_func(**kwargs):
    auth = request.authorization
    user = users.first(email=auth.username)
    if not user:
        raise ProcessingException(message='Unauthorized Access')
    if not verify_and_update_password(auth.password, user):
        raise ProcessingException(message='Unauthorized Access')

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
    
def parser_by_name(name):
    if (name is not None) and (name != ""):
        module_path = ".".join(("keepupwithscience", "parser", name))
        module = importlib.import_module(module_path)
        f = getattr(module,name)
    else:
        from app.scraper.parser import default_parser
        f = getattr(default_parser,"default_parser")
    return f