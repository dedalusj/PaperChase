# -*- coding: utf-8 -*-
"""
    paperchase.papers
    ~~~~~~~~~~~~~~~~~

    paperchase papers package
"""
import datetime

from ..core import Service
from .models import Paper, UserPaper

class PapersService(Service):
    __model__ = Paper
    
class UserPapersService(Service):
    __model__ = UserPaper
    
    def _unreadPapers(self, user):
        return user.papers.filter(UserPaper.read_at == None).all()
        
    def unreadList(self, user):
        return [paper.paper_id for paper in self._unreadPapers(user)]
        
    def markUnread(self, user, paper_ids):
        papers_to_mark = user.papers.filter(UserPaper.paper_id.in_(paper_ids), UserPaper.read_at != None).all()
        ids_changed = []
        for paper in papers_to_mark:
            paper.read_at = None
            self.save(paper)
            ids_changed.append(paper.paper_id)
        return ids_changed
        
    def markRead(self, user, paper_ids):
        papers_to_mark = user.papers.filter(UserPaper.paper_id.in_(paper_ids), UserPaper.read_at == None).all()
        ids_changed = []
        for paper in papers_to_mark:
            paper.read_at = datetime.datetime.utcnow()
            self.save(paper)
            ids_changed.append(paper.paper_id)
        return ids_changed
