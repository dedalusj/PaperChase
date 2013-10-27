import datetime
from flask.ext.restful import Resource, fields, marshal, abort
from flask import request, current_app
from passlib.hash import bcrypt

from ..services import users
from ..core import auth
from ..tasks import send_confirmation_email

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
    def get(self):
        user = users.request_user()
        return marshal(user, user_fields)
        
class RegisterAPI(Resource):
    """API :class:`Resource` for a registering a new user."""
    
    def post(self):
        email = request.json['email']
        user = users.first(email = email)
        if user:
            abort(409)
        password = request.json['password']
        password = bcrypt.encrypt(password, salt = current_app.config['PASSWORD_SALT'])
        user = users.create(email = email, password = password, registered_at = datetime.datetime.utcnow())
        send_confirmation_email.delay(email)
        return marshal(user, user_fields)
