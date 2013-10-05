# -*- coding: utf-8 -*-
"""
    paperchase.helpers
    ~~~~~~~~~~~~~~~~

    paperchase helpers module
"""

import pkgutil
import importlib
import os
from datetime import timedelta
import feedparser
from flask import Blueprint, request, current_app
from passlib.hash import bcrypt

from .core import auth
from .services import users

@auth.get_password
def get_pw(username):
    return users.get_pw(username)

@auth.hash_password
def hash_pw(password):
    """Flask-HTTPAuth method to hash the password."""
    return bcrypt.encrypt(password, salt = current_app.config['PASSWORD_SALT'])

def smart_truncate(content, length=250, suffix='...'):
    if len(content) <= length:
        return content
    return content[:length].rsplit(' ', 1)[0]+suffix

def register_blueprints(app, package_name, package_path):
    """
    Register all Blueprint instances on the specified Flask application found
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
    Returns the number of days between two timestamps.
    
    :param t1: Time one.
    :param t2: Time two.
    """
    timedelta = t1 - t2
    return timedelta.days

def deltatime(period, frequency):
    """
    Returns the :class:`timedelta` given a period and a frequency over which 
    the feed is refreshed in that period.
    
    :param period: the period in the feed RSS
    :param frequency: the frequency of refresh of the feed in the period 
    """
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
    
def splitall(path):
    """
    Split a file path into its components returned as a list.
    
    :param path: a string representing the file path
    """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
    
def assetsList(app, folder = 'js', extension = 'js', exclusions = []):
    """
    Compile a list of assets file of the kind specified by `extension` starting from
    `folder` within the app static folder.
    
    :param app: a :class:`Flask` app
    :param folder: a string specifying the root folder within the app static folder where to search
    :param extension: a string specifying the kind of assets file to search
    :param exclusions: a dictonary containing strings representing the names of files to exclude
    """
    files_list = []
    for root, dirs, files in os.walk(os.path.join(app.static_folder,folder)):
        for file in files:
            if file.endswith("."+extension) and all(file != s for s in exclusions):
                path_parts = splitall(root)
                static_index = path_parts.index("static")
                path_parts = path_parts[static_index+1:]
                path_parts.append(file)
                files_list.append('/'.join(path_parts))
    return files_list