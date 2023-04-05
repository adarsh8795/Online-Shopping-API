from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import CustomerModel
from sqlalchemy.exc import SQLAlchemyError
from schemas import LoginSchema
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from models import SellerModel
from models import DeliverBoyModel

blp = Blueprint("Login", __name__,description = "Login related operations")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self,user_data):
      customer = CustomerModel.query.filter(CustomerModel.email == user_data["email"]).first()
      if customer and pbkdf2_sha256.verify(user_data["password"],customer.password):
         access_token = create_access_token(identity = customer.id,additional_claims={"role" : "user"})  
         return{
            "message" : " customer logged in successfully",
            "access_token" : access_token,
            
         }
      seller = SellerModel.query.filter(SellerModel.email == user_data["email"]).first()
      if seller and pbkdf2_sha256.verify(user_data["password"],seller.password):
         access_token = create_access_token(identity = seller.id,additional_claims={"role" : "seller"})
         return {
            "message" : "seller logged in successfully",
            "access_token" : access_token
         }
      delivery_agent = DeliverBoyModel.query.filter(DeliverBoyModel.email == user_data["email"]).first()
      if delivery_agent and pbkdf2_sha256.verify(user_data["password"],delivery_agent.password):
         access_token = create_access_token(identity = delivery_agent.id,additional_claims={"role" : "deliveryboy"})
         return {"message" : "delivery agent loged in successfully",
                 "access_token" : access_token }
      return{ "message" :" Invalid input " }

