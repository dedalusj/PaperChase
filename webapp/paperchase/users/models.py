# -*- coding: utf-8 -*-
"""
    paperchase.users.models
    ~~~~~~~~~~~~~~~~~~~~~

    User models
"""

from ..core import db
from ..journals import Journal
    
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
    
    def __str__(self):
        return self.email
    
    def subscribe(self, journal):
        if not self.is_subscribed(journal):
            self.subscriptions.append(journal)
            return self
        
    def unsubscribe(self, journal):
        if self.is_subscribed(journal):
            self.subscriptions.remove(journal)
            return self
        
    def is_subscribed(self, journal):
        return self.subscriptions.filter(subscriptions_users.c.journal_id == journal.id).count() > 0