from flask.ext.restful import Resource, fields, marshal
from flask_security import http_auth_required
from ..services import users
#from ..models import *

user_fields = {
    'email': fields.String,
    'id': fields.Integer,
    'registered_at' : fields.DateTime
}

class UserAPI(Resource):
    decorators = [http_auth_required]
    def get(self, email):
        user = users.first(email = email)
        if user is None:
            abort(404)
        return marshal(user, user_fields)