from datetime import *

from flask.ext.restful import Resource, marshal, reqparse
from flask import request, abort, g, url_for

from ..services import user_papers
from ..core import auth
from ..helpers.linkheader import composeLinkHeader
from .fields import paper_fields, full_paper_fields


class PaperListAPI(Resource):

    """
    API :class:`Resource` for a list of papers for the user in the request.
    """

    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('per_page', type=int, default=50)
        self.parser.add_argument('unread', type=bool, default=False)
        self.parser.add_argument('since', type=str)
        self.parser.add_argument('ids', type=str)
        super(PaperListAPI, self).__init__()

    def get(self, journal_id=None):
        args = self.parser.parse_args()
        user = g.user
        paperList = user_papers.grab_papers(user, journal_id, args['unread'],
                                            args['ids'], args['since'])

        paperList = paperList.order_by(user_papers.model().created.desc())
        paperList = paperList.paginate(args['page'], per_page=args['per_page'])
        numberOfPages = paperList.pages

        pageNavigationLinks = {}
        if args['page'] < numberOfPages:
            pageNavigationLinks['last'] = url_for('papers', _external=True,
                                                  per_page=args['per_page'], page=numberOfPages)
        if args['page'] < numberOfPages-1:
            pageNavigationLinks['next'] = url_for('papers', _external=True,
                                                  per_page=args['per_page'], page=args['page']+1)
        if args['page'] > 1:
            pageNavigationLinks['first'] = url_for('papers', _external=True,
                                                   per_page=args['per_page'], page=1)
        if args['page'] > 2:
            pageNavigationLinks['prev'] = url_for('papers', _external=True,
                                                  per_page=args['per_page'], page=args['page']-1)

        return map(lambda p: marshal(p, paper_fields), paperList.items), 200, \
            {'X-Total-Count': str(paperList.pages), 'Link': composeLinkHeader(pageNavigationLinks)}


class PaperAPI(Resource):

    """API :class:`Resource` for a single paper."""

    decorators = [auth.login_required]

    def get(self, id):
        user = g.user
        paper = user.papers.filter_by(paper_id=id).first_or_404()
        return marshal(paper, full_paper_fields)


class UnreadPapersAPI(Resource):

    """API :class:`Resource` to retrieve or mark papers as unread"""

    decorators = [auth.login_required]

    def get(self):
        """Get the list of the unread paper ids"""
        user = g.user
        return user_papers.unreadList(user)

    def put(self):
        """Grab the ids from the request to mark read papers as unread"""
        unread_ids = request.json['unread_papers']
        if len(unread_ids) > 1000:
            abort(413)
        user = g.user
        marked_ids = user_papers.markUnread(user, unread_ids)
        return marked_ids


class ReadPapersAPI(Resource):

    """API :class:`Resource` to mark papers as read"""

    decorators = [auth.login_required]

    def put(self):
        """Put papers in the read list equivalent to marking them as read"""
        read_ids = request.json['readPapers']
        if len(read_ids) > 1000:
            abort(413)
        user = g.user
        marked_ids = user_papers.markRead(user, read_ids)
        return marked_ids


class MarkAllPapersAPI(Resource):

    """API :class:`Resource` to mark all papers as read"""

    decorators = [auth.login_required]

    def put(self):
        """
        Delete papers from the unread list equivalent to marking them as read
        """
        user = g.user
        user_papers.markAllRead(user)
        return ''
