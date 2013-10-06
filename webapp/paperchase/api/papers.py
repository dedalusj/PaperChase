from flask.ext.restful import Resource, fields, marshal, reqparse

from ..services import users, papers
from ..core import auth
from ..helpers import smart_truncate

from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1)
parser.add_argument('per_page', type=int, default=10)
#parser.add_argument('since', type=types.date())
parser.add_argument('unread', type=bool)

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

full_paper_fields = dict(common_paper_fields)
full_paper_fields['abstract'] = fields.String(attribute='paper.abstract')

class PaperListAPI(Resource):
    """API :class:`Resource` for a list of papers for the user in the request."""
    
    decorators = [auth.login_required]
    def get(self):
        args = parser.parse_args()
        user = users.request_user()
        paperList = user.papers.paginate(args['page'],per_page=args['per_page'])
        return map(lambda p: marshal(p, paper_fields), paperList.items)
        
class PaperAPI(Resource):
    """API :class:`Resource` for a single paper."""
    
    decorators = [auth.login_required]
    def get(self,id):
        user = users.request_user()
        paper = user.papers.filter_by(paper_id = id).first_or_404()
        return marshal(paper, full_paper_fields)