# -*- coding: utf-8 -*-
"""
    paperchase.users
    ~~~~~~~~~~~~~~

    paperchase users package
"""
from flask import request

from ..core import Service
from .models import User, subscriptions_users

class UsersService(Service):
    __model__ = User
    
    def get_pw(self,username):
        """Flask-HTTPAuth method to validate a Basic HTTP Authentication."""
        user = self.first(email = username)
        if user:
            return user.password
        return None
    
    def request_user(self):
        """
        Return the :class:`User` corresponding to the username passed
        in the HTTP request.
        """
        return self.first(email = request.authorization.username)
        
    def is_subscribed(self, user, journal):
        return user.subscriptions.filter(subscriptions_users.c.journal_id == journal.id).count() > 0
        
    def subscribe(self, user, journal):
        if not self.is_subscribed(user, journal):
            user.subscriptions.append(journal)
            self.save(user)
            return user
        
    def unsubscribe(self, user, journal):
        if self.is_subscribed(user, journal):
            user.subscriptions.remove(journal)
            self.save(user)
            return user
        
#    def _unreadPapers(self, user):
#        return user.papers.filter(UserPaper.read_at == None).all()
#        
#    def unreadList(self, user):
#        return [paper.paper_id for paper in self._unreadPapers(user)]
#        
#    def markUnread(self, user, paper_ids):
#        papers_to_mark = user.papers.filter(UserPaper.paper_id.in_(paper_ids), UserPaper.read_at != None).all()
#        for paper in papers_to_mark:
#            paper.read_at = None
#        return papers_to_mark
    