from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.delivery_boy import DeliverBoyModel
from schemas import DeliveryBoySchema,OrderSchema
from passlib.hash import pbkdf2_sha256
from helper.email_checker import check
from flask_jwt_extended import jwt_required,get_jwt

blp = Blueprint("DeliveryBoy",__name__, description="Operations on DeliveryBoy")

@blp.route("/delivery_boy")
class DeliveryBoy(MethodView):
    @blp.arguments(DeliveryBoySchema)
    @blp.response(201,DeliveryBoySchema)
    def post(self,deliveryboy_data):
       if check(deliveryboy_data["email"])!= 1 :
            abort (422,message = "invalid Email")
       if(len(deliveryboy_data["password"]) < 7  ):
            abort(422,message = "invalid password input")
       d =  DeliverBoyModel(name = deliveryboy_data["name"] ,email = deliveryboy_data["email"], status = "free" , password = pbkdf2_sha256.hash(deliveryboy_data["password"]))
       db.session.add(d)
       db.session.commit()
       return d
    @blp.response(201,DeliveryBoySchema(many=True))
    def get(self):
        return DeliverBoyModel.query.all()


@blp.route("/deliveryboy/<string:deliveryboy_id>/checkorder")
class CheckOrder(MethodView):
    @blp.response(201,OrderSchema(many=True))
    def get(self,deliveryboy_id):
        delivery_boy = DeliverBoyModel.query.get_or_404(deliveryboy_id)
        return delivery_boy.order.all()
    

