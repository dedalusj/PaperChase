# -*- coding: utf-8 -*-
"""
    paperchase.users.models
    ~~~~~~~~~~~~~~~~~~~~~

    User models
"""

from flask_security import UserMixin, RoleMixin

from ..core import db
from ..journals import Journal

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))
    
subscriptions_users = db.Table(
    'subscriptions_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('journal_id', db.Integer(), db.ForeignKey('journals.id')))


class Role(RoleMixin, db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other and
                self.name != getattr(other, 'name', None))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    subscriptions = db.relationship('Journal', secondary=subscriptions_users, backref=db.backref('users', lazy='dynamic'), lazy = 'dynamic')
    
    def __str__(self):
        return self.email
    
    def subscribe(self, journal):
        if not self.is_subscribed(journal):
            self.subscriptions.append(journal)
            return self
        
    def unsubscribed(self, journal):
        if self.is_subscribed(journal):
            self.subscriptions.remove(journal)
            return self
        
    def is_subscribed(self, journal):
        return self.subscriptions.filter(subscriptions_users.c.journal_id == journal.id).count() > 0