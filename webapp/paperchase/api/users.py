from flask.ext.restful import Resource, fields, marshal
from flask import request
from ..services import users
from ..core import auth

user_fields = {
    'email': fields.String,
    'id': fields.Integer,
    'registered_at' : fields.DateTime
}

class UserAPI(Resource):
    decorators = [auth.login_required]
    def get(self, email):
        user = users.first(email = email)
        return marshal(user, user_fields)
