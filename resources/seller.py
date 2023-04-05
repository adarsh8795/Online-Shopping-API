from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.seller import SellerModel
from models.item import ItemModel
from models.category import CategoryModel
from passlib.hash import pbkdf2_sha256
# from models.itemcategory import ItemCategory
from helper.email_checker import check
from schemas import SellerSchema,SellerUpdateSchema,PlainCategorySchema,OrderSchema
from sqlalchemy.exc import SQLAlchemyError
blp = Blueprint("Sellers",__name__, description="Operations on stores")

@blp.route("/seller")
class Seller(MethodView):
    @blp.arguments(SellerSchema)
    @blp.response(201,SellerSchema)
    def post(self,seller_data):
        if check(seller_data["email"])!= 1 :
            abort (422,message = "invalid Email")
        if(len(seller_data["password"]) < 7  ):
            abort(422,message = "invalid password input")
        obj = SellerModel(name = seller_data["name"] ,email = seller_data["email"], password = pbkdf2_sha256.hash(seller_data["password"]))
        db.session.add(obj)
        db.session.commit()
        return {**seller_data}
    
    @blp.response(200,SellerSchema( many= True))
    def get(self):
       return SellerModel.query.all()
    
@blp.route("/seller/<string:seller_id>/category")
class SellerCategory(MethodView):
    @blp.arguments(PlainCategorySchema)
    @blp.response(201,PlainCategorySchema)
    def post(self,category_data,seller_id):
        s = SellerModel.query.get_or_404(seller_id)
        if(s):
            c = CategoryModel(**category_data)
            db.session.add(c)
            db.session.commit()
            return category_data
        return {"message" : "seller not found"}
    def get(self,seller_id):
        return SellerModel.query.all()
@blp.route("/seller/<string:seller_id>/category/<string:category_id>")
class LinkItemCategory(MethodView):
    def post(self,item_id,category_id):
        item = ItemModel.query.get_or_404(item_id)
        category = CategoryModel.query.get_or_404(category_id)
        category.items.append(item)
        try :
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort (500,message = "failed call")
        return category
    
@blp.route("/seller/<string:seller_id>/checkorder")
class SellerOrderList(MethodView):
    @blp.response(201,OrderSchema(many=True))
    def get(self,seller_id):
        seller = SellerModel.query.get_or_404(seller_id)
        if(seller):
            return seller.order.all()
        return {"message" : "no order"},201
    
#delete item by seller
@blp.route("/seller/<string:seller_id>/item/<string:item_id>")
class ItemOperations(MethodView):
    def delete(self,seller_id,item_id):
        seller = SellerModel.query.get_or_404(seller_id)
        if(seller):
            item = ItemModel.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            return {"message" : "item deleted"}
        else :
            return {"error " : "Invalid input"}
    
        