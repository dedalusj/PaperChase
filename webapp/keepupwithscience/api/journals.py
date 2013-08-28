from flask.ext.restful import Resource, fields, marshal
from ..services import categories, journals
from ..models import Category, Journal
from flask_security import http_auth_required

subcategory_fields = {
    'name': fields.String,
    'uri': fields.Url('category')
}

category_fields = {
    'name': fields.String,
    'uri': fields.Url('category'),
    'subcategories' : fields.List(fields.Nested(subcategory_fields))
}

journal_fields = {
    'title': fields.String,
    'uri': fields.Url('journal'),
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
        return { 'category': marshal(category, category_fields) }
        
class SubcategoryListAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        category = categories.get(id)
        if category is None:
            abort(404)
        subcategoryList = category.subcategories
        return { 'subcategories': map(lambda c: marshal(c, subcategory_fields), subcategoryList) }
        
class CategoryJournalsAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        category = categories.get(id)
        if category is None:
            abort(404)
        journalList = category.journals
        return { 'journals': map(lambda j: marshal(j, journal_fields), journalList) }
        
class JournalListAPI(Resource):
    decorators = [http_auth_required]
    def get(self):
        journalList = journals.all()
        return { 'journals': map(lambda j: marshal(j, journal_fields), journalList) }
        
class JournalAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        journal = journals.get(id)
        if journal is None:
            abort(404)
        return { 'journal': marshal(journal, journal_fields) }