from flask.ext.restful import Resource, fields, marshal
from flask_security import http_auth_required
from flask import request
from sqlalchemy import or_
from sqlalchemy.orm import eagerload
from flask.ext.mail import Message
from ..services import categories, journals, users
from ..models import *
from ..core import mail

from flask import current_app

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

class CategoryListAPI(Resource):
    decorators = [http_auth_required]
    def get(self):
        categoryList = categories.filter(Category.parent_id == None)
        return map(lambda c: marshal(c, category_fields), categoryList)

class CategoryAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        category = categories.get(id)
        if category is None:
            abort(404)
        return marshal(category, category_fields)
        
class SubcategoryListAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        category = categories.get(id)
        if category is None:
            abort(404)
        subcategoryList = category.subcategories
        return map(lambda c: marshal(c, subcategory_fields), subcategoryList)
        
class CategoryJournalsAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        category = categories.get(id)
        if category is None:
            abort(404)
        user = users.first(email = request.authorization.username)
        user_subscriptions = user.subscriptions.all()
        # every request for the journals of a category should return the journals of the parent category as well
        journalList = Journal.query.join(journals_categories, (journals_categories.c.journal_id == Journal.id)).filter(or_(journals_categories.c.category_id == category.id, journals_categories.c.category_id == category.parent_id)).all()
        for j in journalList:
            j.subscribed = (j in user_subscriptions)
        return map(lambda j: marshal(j, journal_fields), journalList)
        
class JournalListAPI(Resource):
    decorators = [http_auth_required]
    def get(self):
        journalList = journals.all()
        return map(lambda j: marshal(j, journal_fields), journalList)
        
class JournalAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        journal = journals.get(id)
        if journal is None:
            abort(404)
        return marshal(journal, journal_fields)
        
class SuggestionAPI(Resource):
    decorators = [http_auth_required]
    def post(self):
        # this should be shipped to celery
        msg = Message('Journal suggestion', sender='youremail@goes.here', recipients=['youremail@goes.here'])
        msg.body = """{0}""".format(str(request.json))
        mail.send(msg)      
        return 201