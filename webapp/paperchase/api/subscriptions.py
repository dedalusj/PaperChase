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
    
    def delete(self):
        current_app.logger.debug(request.headers)
#        journal_id = request.json['journal_id']
#        current_app.logger.debug('Deleted subscription with id: {0}'.format(journal_id))
    #        abort_if_todo_doesnt_exist(todo_id)
    #        del TODOS[todo_id]
        return '', 204