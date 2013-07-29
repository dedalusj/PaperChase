# -*- coding: utf-8 -*-
"""
    keepupwithscience.journals.models
    ~~~~~~~~~~~~~~~~~~~~~~

    Journal models
"""

from ..core import db
from ..helpers import JsonSerializer

journals_categories = db.Table('journals_categories', db.Column('journal_id', db.Integer(), db.ForeignKey('journals.id')), db.Column('category_id', db.Integer(), db.ForeignKey('categories.id')))

class CategoryJsonSerializer(JsonSerializer):
    __json_hidden__ = ['journals']

class Category(CategoryJsonSerializer, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    def __str__(self):
            return self.name

class JournalJsonSerializer(JsonSerializer):
    pass

class Journal(JournalJsonSerializer, db.Model):
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index = True, unique = True)
    short_title = db.Column(db.String(50))
    url = db.Column(db.String(200), index = True, unique = True)
    last_checked = db.Column(db.DateTime)
    update_frequency = db.Column(db.Integer)
    metadata_update = db.Column(db.DateTime)
    papers = db.relationship('Paper', backref = 'journal', lazy = 'dynamic')
    parser_function = db.Column(db.String(50))
    favicon = db.Column(db.String(1024))
    color = db.Column(db.String(7))
    categories = db.relationship('Category', secondary=journals_categories, backref=db.backref('journals', lazy='dynamic'), lazy = 'dynamic')
    
    def __str__(self):
            return self.title