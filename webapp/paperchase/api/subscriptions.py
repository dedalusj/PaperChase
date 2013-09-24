from flask.ext.restful import Resource, fields, marshal
from flask_security import http_auth_required
from flask import request, abort
from ..services import users, journals

from flask import current_app

def request_user():
    return users.first(email = request.authorization.username)


journal_fields = {
    'title': fields.String,
    'id': fields.Integer
}

class SubscriptionListAPI(Resource):
    decorators = [http_auth_required]
    def get(self):
        user = request_user()
        subscriptionsList = user.subscriptions
        return map(lambda j: marshal(j, journal_fields), subscriptionsList)
    
    def post(self):
        journal_id = request.json['journal_id']
        journal = journals.get(journal_id)
        user = request_user()
        users.save(user.subscribe(journal))
        return '', 201
    
class SubscriptionAPI(Resource):
    decorators = [http_auth_required]
    def delete(self,id):
        journal = journals.get(id)
        user = request_user()
        users.save(user.unsubscribe(journal))
        return '', 204