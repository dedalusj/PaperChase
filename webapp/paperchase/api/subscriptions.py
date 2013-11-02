from flask.ext.restful import Resource, fields, marshal
from flask import request

from ..services import users, journals, user_papers
from ..core import auth

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
        journal = journals.get_or_404(journal_id)
        user = users.request_user()
        users.subscribe(user,journal)
        # TODO: this should actually be in the subscribe method but it's a mess
        #       with circular dependencies
        user_papers.user_subscribed(user,journal)
        return '', 201
    
class SubscriptionAPI(Resource):
    """
    API :class:`Resource` for unsuscribing the user from 
    a journal given its id.
    """
    
    decorators = [auth.login_required]
    def delete(self,id):
        journal = journals.get_or_404(id)
        user = users.request_user()
        users.unsubscribe(user,journal)
        # TODO: this should actually be in the unsubscribe method but it's a mess
        #       with circular dependencies
        user_papers.user_unsubscribed(user,journal)
        return '', 204