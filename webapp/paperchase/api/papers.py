from flask.ext.restful import Resource, fields, marshal, reqparse

from ..services import users, papers
from ..core import auth
from ..helpers import smart_truncate

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1)
parser.add_argument('per_page', type=int, default=10)
#parser.add_argument('since', type=types.date())
parser.add_argument('unread', type=bool)

class Ellipsis(fields.Raw):
    def format(self, value):
        return smart_truncate(value)

paper_fields = {
    'title': fields.String(attribute='paper.title'),
    'id': fields.Integer(attribute='paper.id'),
    'authors': fields.String(attribute='paper.authors'),
    'abstract': Ellipsis(attribute='paper.abstract'),
    'journal_id': fields.Integer(attribute='paper.journal_id'),
    'score' : fields.Integer,
    'created' : fields.DateTime,
    'read_at' : fields.DateTime
}

class PaperListAPI(Resource):
    """API :class:`Resource` for a list of papers for the user in the request."""
    
    decorators = [auth.login_required]
    def get(self):
        args = parser.parse_args()
        user = users.request_user()
        paperList = user.papers.paginate(args['page'],per_page=args['per_page'])
        return map(lambda p: marshal(p, paper_fields), paperList.items)