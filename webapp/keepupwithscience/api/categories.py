from flask.ext.restful import Resource, fields, marshal
from ..services import categories
from ..models import Category
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

class CategoryListAPI(Resource):
    decorators = [http_auth_required]
    def get(self):
        categoryList = categories.filter(Category.parent_id == None)
        return { 'categories': map(lambda c: marshal(c, category_fields), categoryList) }

class CategoryAPI(Resource):
    decorators = [http_auth_required]
    def get(self, id):
        category = categories.get(id)
        if category is None:
            abort(404)
        return { 'category': marshal(category, category_fields) }