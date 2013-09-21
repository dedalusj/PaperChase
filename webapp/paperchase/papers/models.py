# -*- coding: utf-8 -*-
"""
    paperchase.papers.models
    ~~~~~~~~~~~~~~~~~~~~~~

    papers models
"""

from ..core import db

class Paper(db.Model):
    __tablename__ = 'papers'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(1024))
    abstract = db.Column(db.Text)
    authors = db.Column(db.String(1024))
    url = db.Column(db.String(150), unique = True)
    doi = db.Column(db.String(100))
    ref = db.Column(db.String(100))
    created = db.Column(db.DateTime)
    journal_id = db.Column(db.Integer, db.ForeignKey('journals.id'))
    
    def __str__(self):
            return self.title