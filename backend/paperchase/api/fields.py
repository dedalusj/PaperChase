from flask.ext.restful import fields, marshal

from ..helpers import smart_truncate


class DictList(fields.List):
    """
    Subclass of Flask-Restful Fields.List to properly create response for a list object
    """
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


class Ellipsis(fields.Raw):
    """
    Subclass of Flask-Restful Fields.Raw to handle truncation of text in json responses
    """
    def format(self, value):
        return smart_truncate(value)

# We collect here all the dictionaries used to represent resources and used by Flask-Restful
# to generate responses

user_fields = {
    'email': fields.String,
    'id': fields.Integer,
    'registered_at': fields.DateTime
}

subcategory_fields = {
    'name': fields.String,
    'id': fields.Integer
}

category_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'subcategories': fields.List(fields.Nested(subcategory_fields))
}

full_journal_fields = {
    'title': fields.String,
    'id': fields.Integer,
    'subscribed': fields.Boolean,
    'favicon': fields.String,
    'categories': DictList(fields.Integer(attribute='id'))
}

essential_journal_fields = {
    'title': fields.String,
    'id': fields.Integer,
    'favicon': fields.String
}

common_paper_fields = {
    'title': fields.String(attribute='paper.title'),
    'id': fields.Integer(attribute='paper.id'),
    'authors': fields.String(attribute='paper.authors'),
    'journalId': fields.Integer(attribute='paper.journal.id'),
    'score': fields.Integer,
    'created': fields.DateTime,
    'readAt': fields.DateTime(attribute='read_at')
}

paper_fields = dict(common_paper_fields)
paper_fields['abstract'] = Ellipsis(attribute='paper.abstract')

full_paper_fields = dict(common_paper_fields)
full_paper_fields['abstract'] = fields.String(attribute='paper.abstract')
full_paper_fields['url'] = fields.String(attribute='paper.url')
full_paper_fields['reference'] = fields.String(attribute='paper.ref')
full_paper_fields['doi'] = fields.String(attribute='paper.doi')
