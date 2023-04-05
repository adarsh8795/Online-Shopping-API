from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.customer import CustomerModel
from sqlalchemy.exc import SQLAlchemyError
from helper.email_checker import check
from passlib.hash import pbkdf2_sha256
# from models.cart import CartModel
from schemas import UserSchema,UserUpdateSchema,ItemSchema,CartSchema,OrderSchema,PlainItemSchema,CheckOrderSchema
from models import ItemModel,OrderModel,Sellerorder,DeliverBoyModel,CustomerOrderModel
from models import CartItem
import random
from flask_jwt_extended import jwt_required,get_jwt
# from flask import jsonify

blp = Blueprint("Customers",__name__, description="Operations on stores")

@blp.route("/customer")
class Customer(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,customer_data):
        if check(customer_data["email"])!= 1 :
            abort (422,message = "invalid Email")
        if(len(customer_data["password"]) < 7  ):
            abort(422,message = "invalid password input")

        c1=CustomerModel(name = customer_data["name"] ,email = customer_data["email"], password = pbkdf2_sha256.hash(customer_data["password"]))
        db.session.add(c1)
        db.session.commit()
        return {**customer_data}
    @blp.response(200,UserSchema(many =True ))
    def get(self):
        return CustomerModel.query.all() 
    
#view all items
@blp.route("/customer/<string:customer_id>/item")
class CustomerItemList(MethodView):
    @blp.response(200,ItemSchema(many = True ))
    def get(self,customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        if(customer): 
          return ItemModel.query.all()
        else:
            return{"message" : " customer not exist"}

#add item to cart
#remove item from cart
@blp.route("/customer/<string:customer_id>/item/<string:item_id>")
class CustomerItem(MethodView):

    # @jwt_required()
    @blp.response(201,ItemSchema)
    def post(self,customer_id,item_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        item = ItemModel.query.get_or_404(item_id)
        customer.cart.append(item)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="failed.")
        return item
    def delete(self,customer_id,item_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        item = ItemModel.query.get_or_404(item_id)
        customer.cart.remove(item)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message = "failed")
        return {"message" : "item removed from cart"}

#checkcart
@blp.route("/customer/<string:customer_id>/cart")
class CustomerCart(MethodView):
    @blp.response(201,CartSchema)
    @blp.response(201,ItemSchema(many=True))
    def get(self,customer_id):
        user = CustomerModel.query.get_or_404(customer_id)
        cart_value = 0
        for i in user.cart:
            cart_value += i.price
        return user.cart
    
        
@blp.route("/customer/<string:customer_id>/placeorder")
class CustomerPlaceOrder(MethodView):
    # @jwt_required()
    @blp.arguments(OrderSchema)
    @blp.response(201,OrderSchema)
    def post(self,address,customer_id):
        # claim = get_jwt()
        # if claim["role"] !="user" or claim["sub"] != int(customer_id):
        #     abort(401,message = "unauthorized")
        user = CustomerModel.query.get_or_404(customer_id)
        
        cart = user.cart
        mylist = []
        mylist = user.cart
        if mylist == []:
            abort (400,message = "cart is empty" )
        cart_value = 0
        x = random.randint(1,3)
        # delivery_boy =  DeliverBoyModel.query.get(x)
        for i in user.cart:
            cart_value += i.price
        
        order = OrderModel(
            customer_id = customer_id,
            order_value = cart_value,
            deliveryboy_id = x,
            delivery_address = address["delivery_address"]
            
        )
        db.session.add(order)
        db.session.commit()
        for i in user.cart:
            # item = ItemModel.query.get_or_404(i.id)
            newcart = CustomerOrderModel(
                customer_id = customer_id,
                item_id = i.id,
                order_id = order.id,
                seller_id = i.seller_id
            )
            x = Sellerorder.query.filter(Sellerorder.order_id == order.id,Sellerorder.seller_id == i.seller_id)
            if(x):
                seller_order = Sellerorder(
                    seller_id = i.seller_id,
                    order_id = order.id  
                )
                db.session.add(seller_order)
                db.session.commit()
                
            # else :
                # seller_order = Sellerorder(
                #     seller_id = i.seller_id,
                #     order_id = order.id  
                # )
                # db.session.add(seller_order)
                # db.session.commit()
            
            # print(seller_order)
            
            db.session.add(newcart)
            db.session.commit()
            # print(mylist)
        user.cart = []

        db.session.commit()
        return order
        # return {"message" :"order placed hurray","order_value": cart_value}
     

@blp.route("/customer/<string:customer_id>/checkorder")
class CheckOrder(MethodView):
    @blp.response(201,OrderSchema(many=True))
    def get(self,customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        return customer.order.all()
        # return customer.order.cart()
                
                




