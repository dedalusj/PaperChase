import datetime
from flask.ext.restful import Resource, fields, marshal
from flask import request, current_app
from passlib.hash import bcrypt

from ..services import users
from ..core import auth
from ..helpers import request_user

user_fields = {
    'email': fields.String,
    'id': fields.Integer,
    'registered_at' : fields.DateTime
}

class UserAPI(Resource):
    """
    API :class:`Resource` for a returning the details of a user.
    This endpoint can be used to verify a user login credentials.
    """
    
    decorators = [auth.login_required]
    def get(self, email):
        user = request_user()
        return marshal(user, user_fields)
        
class RegisterAPI(Resource):
    """API :class:`Resource` for a registering a new user."""
    
    def post(self):
        # TODO: This should send a confirmation email
        email = request.json['email']
        password = request.json['password']
        password = bcrypt.encrypt(password, salt = current_app.config['PASSWORD_SALT'])
        user = users.create(email = email, password = password, registered_at = datetime.datetime.utcnow())
        return marshal(user, user_fields)
