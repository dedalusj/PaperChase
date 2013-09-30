from flask.ext.restful import Resource, fields, marshal
from flask import request, abort
from sqlalchemy import or_
from sqlalchemy.orm import eagerload
from ..services import categories, journals, users
from ..models import *
from ..core import auth
from ..tasks import send_suggestion_email

subcategory_fields = {
    'name': fields.String,
    'id': fields.Integer
}

category_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'subcategories' : fields.List(fields.Nested(subcategory_fields))
}

journal_fields = {
    'title': fields.String,
    'id': fields.Integer,
    'subscribed': fields.Boolean
}

def get_category(id):
    category = categories.get(id)
    if category is None:
        abort(404)
    return category

class CategoryListAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        categoryList = categories.filter(Category.parent_id == None)
        return map(lambda c: marshal(c, category_fields), categoryList)

class CategoryAPI(Resource):
    decorators = [auth.login_required]
    def get(self, id):
        category = get_category(id)
        return marshal(category, category_fields)
        
class SubcategoryListAPI(Resource):
    decorators = [auth.login_required]
    def get(self, id):
        category = get_category(id)
        subcategoryList = category.subcategories
        return map(lambda c: marshal(c, subcategory_fields), subcategoryList)
        
class CategoryJournalsAPI(Resource):
    decorators = [auth.login_required]
    def get(self, id):
        category = get_category(id)
        user = users.first(email = request.authorization.username)
        user_subscriptions = user.subscriptions.all()
        # every request for the journals of a category should return the journals of the parent category as well
        journalList = Journal.query.join(journals_categories, (journals_categories.c.journal_id == Journal.id)).filter(or_(journals_categories.c.category_id == category.id, journals_categories.c.category_id == category.parent_id)).all()
        for j in journalList:
            j.subscribed = (j in user_subscriptions)
        return map(lambda j: marshal(j, journal_fields), journalList)
        
class JournalListAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        journalList = journals.all()
        return map(lambda j: marshal(j, journal_fields), journalList)
        
class JournalAPI(Resource):
    decorators = [auth.login_required]
    def get(self, id):
        journal = journals.get(id)
        if journal is None:
            abort(404)
        return marshal(journal, journal_fields)
        
class SuggestionAPI(Resource):
    decorators = [auth.login_required]
    def post(self):
        send_suggestion_email.delay(request.json)
        return 201