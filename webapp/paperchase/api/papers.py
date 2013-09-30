from flask.ext.restful import Resource, fields, marshal, reqparse, types
from flask import request, abort
from ..services import users, papers
from ..core import auth
from ..helpers import request_user

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1)
parser.add_argument('per_page', type=int, default=5)
#parser.add_argument('since', type=types.date())
parser.add_argument('unread', type=bool)

paper_fields = {
    'title': fields.String,
    'id': fields.Integer,
    'authors': fields.String,
    'abstract': fields.String,
    'journal_id': fields.Integer
}

class PaperListAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        args = parser.parse_args()
        user = request_user()
        paperList = user.papers().paginate(args['page'],per_page=args['per_page'])
        return map(lambda p: marshal(p, paper_fields), paperList.items)