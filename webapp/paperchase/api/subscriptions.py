from flask.ext.restful import Resource, fields, marshal
from flask import request

from ..services import users, journals
from ..core import auth
#from ..helpers import request_user

journal_fields = {
    'title': fields.String,
    'id': fields.Integer
}

class SubscriptionListAPI(Resource):
    """API :class:`Resource` for a the user subscriptions."""
    
    decorators = [auth.login_required]
    def get(self):
        """Returns the list of journals the user is subscribed to."""
        
        user = users.request_user()
        subscriptionsList = user.subscriptions
        return map(lambda j: marshal(j, journal_fields), subscriptionsList)
    
    def post(self):
        """Post request with the journal id the user wants to subscribe to."""
        
        journal_id = request.json['journal_id']
        journal = journals.get(journal_id)
        user = users.request_user()
        users.save(user.subscribe(journal))
        return '', 201
    
class SubscriptionAPI(Resource):
    """
    API :class:`Resource` for unsuscribing the user from 
    a journal given its id.
    """
    
    decorators = [auth.login_required]
    def delete(self,id):
        journal = journals.get(id)
        user = users.request_user()
        users.save(user.unsubscribe(journal))
        return '', 204