# -*- coding: utf-8 -*-
"""
    paperchase.users.models
    ~~~~~~~~~~~~~~~~~~~~~

    User models
"""
from flask import current_app, g
from passlib.hash import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,\
    BadSignature, SignatureExpired

from ..core import db, auth

subscriptions_users = db.Table(
    'subscriptions_users',
    db.Column('user_id', db.Integer(),
              db.ForeignKey('users.id'), nullable=False),
    db.Column('journal_id',
              db.Integer(),
              db.ForeignKey('journals.id'),
              nullable=False))


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    registered_at = db.Column(db.DateTime())

    subscriptions = db.relationship(
        'Journal',
        secondary=subscriptions_users,
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic')
    papers = db.relationship(
        "UserPaper", backref=db.backref('users'), lazy='dynamic')

    def __str__(self):
        return self.email

    @staticmethod
    def hash_password(password):
        return bcrypt.encrypt(password, salt=current_app.config['PASSWORD_SALT'])

    def verify_password(self, password):
        return self.password == bcrypt.encrypt(
            password, salt=current_app.config['PASSWORD_SALT'])

    def generate_auth_token(self, expiration=7200):  # two hours expiration
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        # TODO
        # we should also keep track of when a user change her password and dump that
        # into the token. When she changes her password a previously released token
        # becomes invalid. It's a compromise between dumping the password in the token
        # (insecure) and having just the email which doesn't protect the user from
        # stolen passwords
        return s.dumps({'email': self.email})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.filter_by(email=data['email']).first()
        return user
