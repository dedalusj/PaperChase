from flask import request, current_app, g
from flask.ext.restful import Resource, fields, marshal

from ..services import categories, journals
from ..core import auth
from ..tasks import send_email

subcategory_fields = {
    'name': fields.String,
    'id': fields.Integer
}

category_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'subcategories': fields.List(fields.Nested(subcategory_fields))
}

journal_fields = {
    'title': fields.String,
    'id': fields.Integer,
    'subscribed': fields.Boolean
}


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


class SubcategoryListAPI(Resource):

    """API :class:`Resource` for a list of subcategories given a category id."""

    decorators = [auth.login_required]

    def get(self, id):
        category = categories.get_or_404(id)
        subcategoryList = category.subcategories
        return map(lambda c: marshal(c, subcategory_fields), subcategoryList)


class CategoryJournalsAPI(Resource):

    """API :class:`Resource` for a list of journals for a category id."""

    decorators = [auth.login_required]

    def get(self, id):
        user = g.user
        user_subscriptions = user.subscriptions.all()
        category = categories.get_or_404(id)
        journalList = categories.all_journals(category).all()
        for j in journalList:
            j.subscribed = (j in user_subscriptions)
        return map(lambda j: marshal(j, journal_fields), journalList)


class JournalListAPI(Resource):

    """API :class:`Resource` for a list of journals."""

    decorators = [auth.login_required]

    def get(self):
        journalList = journals.all()
        return map(lambda j: marshal(j, journal_fields), journalList)


class JournalAPI(Resource):

    """API :class:`Resource` for a single journal given its id."""

    decorators = [auth.login_required]

    def get(self, id):
        journal = journals.get_or_404(id)
        return marshal(journal, journal_fields)


class SuggestionAPI(Resource):

    """
    API :class:`Resource` for receiving a post request with the details
    of a new journal.
    """

    decorators = [auth.login_required]

    def post(self):
        send_email.delay('Journal Suggestion', 'suggestion', current_app.config[
                         'DEFAULT_MAIL_SENDER'], json_msg=request.json)
        return '', 201
