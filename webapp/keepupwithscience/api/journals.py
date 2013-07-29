# -*- coding: utf-8 -*-
"""
    keepupwithscience.api.journals
    ~~~~~~~~~~~~~~~~~~~~~

    Journals endpoints
"""

from flask import Blueprint, request

from ..services import journals, categories
from . import KeepUpWithScienceFormError, route

journals_bp = Blueprint('journals', __name__, url_prefix='/journals')

@route(journals_bp, '/')
def list():
    """Returns a list of journals instances."""
    return journals.all()

@route(journals_bp, '/<journal_id>')
def show(journal_id):
    """Returns a journal instance."""
    return journals.get_or_404(journal_id)
    
categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@route(categories_bp, '/')
def list():
    """Returns a list of categories instances."""
    return categories.all()

@route(categories_bp, '/<category_id>')
def show(category_id):
    """Returns a category instance."""
    return categories.get_or_404(category_id)