import datetime
from flask.ext.restful import Resource, fields, marshal
from flask import request, current_app
from passlib.hash import bcrypt

from ..services import users
from ..core import auth
from ..models import User

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
        
class RegisterAPI(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        password = bcrypt.encrypt(password, salt = current_app.config['PASSWORD_SALT'])
        # decode both email and password using hashing algorithm against the csrf_token
        user = users.create(email = email, password = password, registered_at = datetime.datetime.utcnow())
        return marshal(user, user_fields)
