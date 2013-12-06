from flask import request, current_app, g
from flask.ext.restful import Resource, fields, marshal, reqparse

from ..services import categories, journals
from ..core import auth
from ..tasks import send_email


class DictList(fields.List):
    def output(self, key, data):
        value = fields.get_value(key if self.attribute is None else self.attribute, data)
        # we cannot really test for external dict behavior
        if fields.is_indexable_but_not_string(value) and not isinstance(value, dict):
            # Convert all instances in typed list to container type
            return [self.container.output(idx, val) for idx, val
                    in enumerate(value)]

        if value is None:
            return self.default

        return [marshal(value, self.container.nested)]


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
    'categories': DictList(fields.Integer(attribute='id'))
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


class JournalListAPI(Resource):

    """API :class:`Resource` for a list of journals."""

    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('subscribed', type=bool, default=False)
        super(JournalListAPI, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        if args.subscribed is False:
            return map(lambda j: marshal(j, journal_fields), journals.all())
        extended_fields = journal_fields.copy()
        extended_fields.update({'subscribed': fields.Boolean})
        journalList = journals.all(user=g.user)
        return map(lambda j: marshal(j, extended_fields), journalList)


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
