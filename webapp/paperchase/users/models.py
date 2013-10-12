# -*- coding: utf-8 -*-
"""
    paperchase.users.models
    ~~~~~~~~~~~~~~~~~~~~~

    User models
"""

from ..core import db

subscriptions_users = db.Table(
    'subscriptions_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable = False),
    db.Column('journal_id', db.Integer(), db.ForeignKey('journals.id'), nullable = False))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    registered_at = db.Column(db.DateTime())

    subscriptions = db.relationship('Journal', secondary=subscriptions_users, backref=db.backref('users', lazy='dynamic'), lazy = 'dynamic')
    papers = db.relationship("UserPaper", backref=db.backref('users'), lazy='dynamic')
    
    def __str__(self):
        return self.email                        