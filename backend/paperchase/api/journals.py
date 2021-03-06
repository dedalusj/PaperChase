from flask import request, current_app, g
from flask.ext.restful import Resource, marshal

from ..services import categories, journals
from ..core import auth
from ..tasks import send_email
from .fields import category_fields, full_journal_fields


class CategoryListAPI(Resource):

    """API :class:`Resource` for a list of categories."""

    decorators = [auth.login_required]

    def get(self):
        categoryList = categories.find(parent_id=None)
        return map(lambda c: marshal(c, category_fields), categoryList)


class CategoryAPI(Resource):

    """API :class:`Resource` for a single category given its id."""

    decorators = [auth.login_required]

    def get(self, id):
        category = categories.get_or_404(id)
        return marshal(category, category_fields)


class JournalListAPI(Resource):

    """API :class:`Resource` for a list of journals."""

    decorators = [auth.login_required]

    def get(self):
        journalList = journals.all(g.user)
        return map(lambda j: marshal(j, full_journal_fields), journalList)


class JournalAPI(Resource):

    """API :class:`Resource` for a single journal given its id."""

    decorators = [auth.login_required]

    def get(self, id):
        journal = journals.get_or_404(id)
        return marshal(journal, full_journal_fields)


class SuggestionAPI(Resource):

    """
    API :class:`Resource` for receiving a post request with the details
    of a new journal.
    """

    decorators = [auth.login_required]

    def post(self):
        send_email.delay('Journal Suggestion', 'suggestion', current_app.config[
                         'MAIL_DEFAULT_SENDER'], json_msg=request.json)
        return '', 201
