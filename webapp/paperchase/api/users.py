from flask.ext.restful import Resource, fields, marshal
from flask_security import http_auth_required
from flask import request
from ..services import users

user_fields = {
    'email': fields.String,
    'id': fields.Integer,
    'registered_at' : fields.DateTime
}

class UserAPI(Resource):
    decorators = [http_auth_required]
    def get(self, email):
        user = users.first(email = email)
        return marshal(user, user_fields)
