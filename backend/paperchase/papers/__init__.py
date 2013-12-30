# -*- coding: utf-8 -*-
"""
    paperchase.papers
    ~~~~~~~~~~~~~~~~~

    paperchase papers package
"""
import datetime
from flask import current_app

from ..core import Service, db
from .models import Paper, UserPaper


class PapersService(Service):
    __model__ = Paper


class UserPapersService(Service):
    __model__ = UserPaper

    def _unreadPapers(self, user):
        return user.papers.filter(UserPaper.read_at == None).order_by(UserPaper.created.desc()).all()

    def unreadList(self, user):
        return [paper.paper_id for paper in self._unreadPapers(user)]

    def markUnread(self, user, paper_ids):
        papers_to_mark = user.papers.filter(
            UserPaper.paper_id.in_(paper_ids), UserPaper.read_at != None).all()
        ids_changed = []
        for paper in papers_to_mark:
            paper.read_at = None
            self.save(paper)
            ids_changed.append(paper.paper_id)
        return ids_changed

    def markRead(self, user, paper_ids):
        papers_to_mark = user.papers.filter(
            UserPaper.paper_id.in_(paper_ids), UserPaper.read_at == None).all()
        ids_changed = []
        for paper in papers_to_mark:
            paper.read_at = datetime.datetime.utcnow()
            self.save(paper)
            ids_changed.append(paper.paper_id)
        return ids_changed

    def markAllRead(self, user):
        user.papers.filter(UserPaper.read_at == None).update(
            {"read_at": datetime.datetime.utcnow()})
        self.commit_changes()

    def user_subscribed(self, user, journal):
        """
        When a user subscribe to a new journal we want to create a new UserPaper object to append to
        his/her list of papers for every paper published in that journal in the last
        SUBSCRIPTION_IMPORT weeks
        """
        weeks = current_app['SUBSCRIPTION_IMPORT']
        papers = journal.papers.filter(
            Paper.created > datetime.datetime.utcnow() - datetime.timedelta(weeks=weeks)).all()
        user_papers = []
        for paper in papers:
            user_papers.append(
                self.new(score=50, created=paper.created, paper_id=paper.id, user_id=user.id))
            self.save_all(user_papers)

    def user_unsubscribed(self, user, journal):
        """
        When a user unsubscribe from a journal we remove all the papers from that journal
        """

        paperQuery = db.session.query(Paper.id).filter(Paper.journal_id == journal.id)

        db.session.query(UserPaper)\
                  .filter(UserPaper.paper_id.in_(paperQuery.subquery()))\
                  .filter(UserPaper.user_id == user.id)\
                  .delete(synchronize_session='fetch')
        self.commit_changes()

        # TODO: we should be able to do a batch delete from the query wihtout
        # looping through all the results
        # papers = db.session.query(UserPaper).join(Paper, (UserPaper.paper_id == Paper.id)).filter(
        #     UserPaper.user_id == user.id, Paper.journal_id == journal.id)
        # for paper in papers:
        #     self.delete(paper)
