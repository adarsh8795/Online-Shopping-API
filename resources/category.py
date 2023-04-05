from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.category import CategoryModel
from schemas import PlainCategorySchema,PlainItemSchema,ItemSchema
from models.item import ItemModel


blp = Blueprint("Category",__name__, description="Operations on category")

@blp.route("/category")
class Category(MethodView):
    @blp.arguments(PlainCategorySchema)
    @blp.response(201,PlainCategorySchema)
    def post(self,category_name):
        try:
            c = CategoryModel(**category_name)
            db.session.add(c)
            db.session.commit()
            return c
        except:
            abort(503,message = "internal error")


    @blp.response(200,PlainCategorySchema(many =True))
    def get(self):
        try:
           return CategoryModel.query.all()
        except:
            abort(503,message = "internal error")
    
@blp.route("/category/<string:category_id>/item")
class CategoryItem(MethodView):
    @blp.response(201,PlainItemSchema)
    def get(self,category_id):
        c = CategoryModel.query.get_or_404(category_id)
        return c.items.all()
    
@blp.route("/item/<string:item_id>/category/<string:category_id>")
class AddCategoryToItem(MethodView):
    @blp.response(201,ItemSchema)
    def post(self,item_id,category_id):
        item = ItemModel.query.get_or_404(item_id)
        if(item):
           item.category_id= category_id
           db.session.commit()
           return item
        else:
            return {"message ": "Invalidinput"}
        



