# -*- coding: utf-8 -*-
"""
    paperchase.journals.models
    ~~~~~~~~~~~~~~~~~~~~~~

    Journal models
"""
from ..core import db

# many-to-many relationship table between categories and journals
journals_categories = db.Table('journals_categories',
                               db.Column('journal_id',
                                         db.Integer(),
                                         db.ForeignKey('journals.id')),
                               db.Column('category_id',
                                         db.Integer(),
                                         db.ForeignKey('categories.id')))


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    parent_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    subcategories = db.relationship(
        'Category',
        lazy='dynamic',
        backref=db.backref('parent', remote_side=[id]))

    def __str__(self):
        return self.name


class Journal(db.Model):
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    short_title = db.Column(db.String(50))
    url = db.Column(db.String(200), index=True, unique=True)
    last_checked = db.Column(db.DateTime)
    next_check = db.Column(db.DateTime)
    metadata_update = db.Column(db.DateTime)
    papers = db.relationship('Paper', backref='journal', lazy='dynamic')
    paths = db.relationship('Path', backref='journal', lazy='dynamic')
    favicon = db.Column(db.String(1024))
    categories = db.relationship('Category', secondary=journals_categories,
                                 backref=db.backref('journals', lazy='dynamic'),
                                 lazy='dynamic')

    def __str__(self):
        return self.title


class Path(db.Model):
    __tablename__ = 'paths'

    id = db.Column(db.Integer, primary_key=True)
    journal_id = db.Column(db.Integer, db.ForeignKey('journals.id'))
    type = db.Column(db.String(15))
    path = db.Column(db.String(300))
