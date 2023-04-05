from db import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_value = db.Column(db.Float(precision=2), unique=False, nullable=False)
    delivery_address = db.Column(db.String(80))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    customer = db.relationship("CustomerModel", back_populates = "order" )
    seller = db.relationship("SellerModel", back_populates = "order",secondary = "sellerorder" )
    deliveryboy_id = db.Column(db.Integer, db.ForeignKey("deliveryboy.id"))
    deliveryboy = db.relationship("DeliverBoyModel", back_populates = "order")
    cart = db.relationship("CustomerOrderModel",backref = "orders" ,lazy = "dynamic")

    
