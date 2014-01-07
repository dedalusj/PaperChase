# -*- coding: utf-8 -*-
"""
    paperchase.papers.models
    ~~~~~~~~~~~~~~~~~~~~~~

    papers models
"""
from ..core import db
from ..models import Journal


class Paper(db.Model):
    __tablename__ = 'papers'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1024))
    abstract = db.Column(db.Text)
    authors = db.Column(db.String(1024))
    url = db.Column(db.String(150), unique=True)
    doi = db.Column(db.String(100))
    ref = db.Column(db.String(100))
    created = db.Column(db.DateTime)
    journal_id = db.Column(db.Integer, db.ForeignKey('journals.id'))

    def __str__(self):
            return self.title

    def __init__(self, **kwargs):
        super(Paper, self).__init__(**kwargs)
        journal = Journal.query.get(kwargs['journal_id'])
        users = journal.users
        for user in users:
            user_paper = UserPaper(score=50, created=kwargs['created'])
            user_paper.paper = self
            user.papers.append(user_paper)


class UserPaper(db.Model):
    __tablename__ = 'userpapers'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), primary_key=True)
    paper = db.relationship("Paper", backref=db.backref('user_paper'))
    created = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    score = db.Column(db.Integer)
