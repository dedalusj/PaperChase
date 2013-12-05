import datetime
from flask.ext.restful import Resource, fields, marshal, abort
from flask import request, current_app, g

from ..services import users
from ..core import auth
from ..tasks import send_email

user_fields = {
    'email': fields.String,
    'id': fields.Integer,
    'registered_at': fields.DateTime
}


class UserAPI(Resource):

    """
    API :class:`Resource` for returning the details of a user.
    This endpoint can be used to verify a user login credentials.
    """

    decorators = [auth.login_required]

    def get(self):
        user = g.user
        return marshal(user, user_fields)


class UserToken(Resource):

    """
    API :class:`Resource` for returning the authentication token
    of a user.
    """

    decorators = [auth.login_required]

    def get(self):
        duration = 7200
        token = g.user.generate_auth_token(duration)
        return {'token': token.decode('ascii'), 'duration': duration}


class RegisterAPI(Resource):

    """API :class:`Resource` for a registering a new user."""

    def post(self):
        email = request.json['email']
        user = users.first(email=email)
        if user:
            abort(409)  # user exists
        password = request.json['password']
        password = users.hash_pw(password)
        user = users.create(
            email=email,
            password=password,
            registered_at=datetime.datetime.utcnow())
        send_email.delay('Paperchase registration', 'registration',
                         email, email=email,
                         domain=current_app.config['DOMAIN'])
        return marshal(user, user_fields)
