from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from models import SellerModel,CategoryModel
from schemas import ItemSchema,ItemUpdateSchema,PlainItemSchema,PlainCategorySchema,CategorySchema
from flask_jwt_extended import jwt_required,get_jwt

blp = Blueprint("Items",__name__, description="Operations on stores")


#create item and get all items
@blp.route("/seller/<string:seller_id>/item")
class Seller_Item(MethodView):
    @blp.response(201,PlainItemSchema)
    @blp.arguments(PlainItemSchema) 
    def post(self,item_data,seller_id):
            # s= SellerModel.query.filter(SellerModel.id == seller_id).first
            item_object=ItemModel(
                price = item_data["price"],
                name = item_data["name"],
                seller_id=seller_id)
            db.session.add(item_object)
            db.session.commit()
            return item_data

    @blp.response(200,PlainItemSchema(many = True))
    def get(self,seller_id):
       seller = SellerModel.query.get_or_404(seller_id)
       return seller.items.all()


    


        
