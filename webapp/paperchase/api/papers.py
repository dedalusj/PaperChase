from dateutil.parser import *
from datetime import *
import pytz

from flask.ext.restful import Resource, fields, marshal, reqparse
from flask import request

from ..services import users, user_papers
from ..core import auth
from ..helpers import smart_truncate

from flask import current_app

class Ellipsis(fields.Raw):
    def format(self, value):
        return smart_truncate(value)

journal_fields = {
    'title': fields.String,
    'id': fields.Integer
}

common_paper_fields = {
    'title': fields.String(attribute='paper.title'),
    'id': fields.Integer(attribute='paper.id'),
    'authors': fields.String(attribute='paper.authors'),
    'journal': fields.Nested(journal_fields,attribute='paper.journal'),
    'score' : fields.Integer,
    'created' : fields.DateTime,
    'read_at' : fields.DateTime
}


paper_fields = dict(common_paper_fields)
paper_fields['abstract'] = Ellipsis(attribute='paper.abstract')

class PaperListAPI(Resource):
    """API :class:`Resource` for a list of papers for the user in the request."""
    
    decorators = [auth.login_required]
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('per_page', type=int, default=10)
        self.parser.add_argument('unread', type=bool, default = False)
        self.parser.add_argument('since', type=str)
        self.parser.add_argument('ids', type=str)
        super(PaperListAPI, self).__init__()
    
    def get(self):    
        args = self.parser.parse_args()
        user = users.request_user()
        paperList = user.papers
        
        if args['unread'] is True:
            paperList = paperList.filter(user_papers.model().read_at == None)
        if args['ids'] is not None:
            ids = [int(id) for id in args['ids'].split(',')]
            paperList = paperList.filter(user_papers.model().paper_id.in_(ids))
        if args['since'] is not None:    
            since = parse(args['since'])
            since = since.replace(tzinfo=None)
            paperList = paperList.filter(user_papers.model().created >= since)
        
        paperList = paperList.order_by(user_papers.model().created.desc())
        paperList = paperList.paginate(args['page'],per_page=args['per_page'])
        return map(lambda p: marshal(p, paper_fields), paperList.items)


full_paper_fields = dict(common_paper_fields)
full_paper_fields['abstract'] = fields.String(attribute='paper.abstract')
full_paper_fields['url'] = fields.String(attribute='paper.url')
full_paper_fields['reference'] = fields.String(attribute='paper.ref')
full_paper_fields['doi'] = fields.String(attribute='paper.doi')
        
class PaperAPI(Resource):
    """API :class:`Resource` for a single paper."""
    
    decorators = [auth.login_required]
    def get(self,id):
        user = users.request_user()
        paper = user.papers.filter_by(paper_id = id).first_or_404()
        return marshal(paper, full_paper_fields)

        
class UnreadPapersAPI(Resource):
    """API :class:`Resource` to mark retrieve or mark papers as unread"""

    decorators = [auth.login_required]
    def get(self):
        """Get the list of the unread paper ids"""
        user = users.request_user()
        return user_papers.unreadList(user)
        
    def put(self):
        """Grab the ids from the request to mark read papers as unread"""
        unread_ids = request.json['unread_papers']
        if len(unread_ids) > 1000:
            return 413
        user = users.request_user()
        marked_ids = user_papers.markUnread(user, unread_ids)
        return marked_ids


class ReadPapersAPI(Resource):
    """API :class:`Resource` to mark papers as read"""
    
    def put(self):
        """Put papers in the read list equivalent to marking them as read"""
        read_ids = request.json['read_papers']
        if len(read_ids) > 1000:
            return 413
        user = users.request_user()
        marked_ids = user_papers.markRead(user, read_ids)
        return marked_ids
        
class MarkAllPapersAPI(Resource):
    """API :class:`Resource` to mark all papers as read"""
    
    def put(self):
        """Delete papers from the unread list equivalent to marking them as read"""
        user = users.request_user()
        user_papers.markAllRead(user)
        return 202
