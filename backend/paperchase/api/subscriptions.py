from flask.ext.restful import Resource, marshal
from flask import request, g

from ..services import users, journals, user_papers
from ..core import auth
from .fields import essential_journal_fields, full_journal_fields


class SubscriptionListAPI(Resource):

    """API :class:`Resource` for a the user subscriptions."""

    decorators = [auth.login_required]

    def get(self):
        """Returns the list of journals the user is subscribed to."""

        user = g.user
        subscriptionsList = user.subscriptions.order_by(journals.__model__.id)
        return map(lambda j: marshal(j, essential_journal_fields), subscriptionsList)

    def post(self):
        """Post request with the journal id the user wants to subscribe to."""
        # TODO: rather slow because of the import of the papers from a journal into a user
        journal_id = request.json['journalId']
        journal = journals.get_or_404(journal_id)
        user = g.user
        users.subscribe(user, journal)
        user_papers.user_subscribed(user, journal)
        journal.subscribed = True
        return marshal(journal, full_journal_fields), 201


class SubscriptionAPI(Resource):

    """
    API :class:`Resource` for unsuscribing the user from
    a journal given its id.
    """

    decorators = [auth.login_required]

    def delete(self, id):
        journal = journals.get_or_404(id)
        user = g.user
        users.unsubscribe(user, journal)
        user_papers.user_unsubscribed(user, journal)
        return '', 204
