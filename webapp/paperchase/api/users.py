from flask.ext.restful import Resource, fields, marshal
from flask_security import http_auth_required
from flask import request
from ..services import users
#from ..models import *

user_fields = {
    'email': fields.String,
    'id': fields.Integer,
    'registered_at' : fields.DateTime
}

journal_fields = {
    'title': fields.String,
    'id': fields.Integer
}

class UserAPI(Resource):
    decorators = [http_auth_required]
    def get(self, email):
        user = users.first(email = email)
        return marshal(user, user_fields)
        
class SubscriptionListAPI(Resource):
    decorators = [http_auth_required]
    def get(self):
        user = users.first(email = request.authorization.username)
        subscriptionsList = user.subscriptions
        return map(lambda j: marshal(j, journal_fields), subscriptionsList)