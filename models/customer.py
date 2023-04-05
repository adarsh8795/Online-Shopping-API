from db import db


class CustomerModel(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80),unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    cart = db.relationship("ItemModel",back_populates = "customer" ,secondary = "cartitem" ,cascade="all ,delete")
    order = db.relationship("OrderModel", back_populates = "customer",lazy = "dynamic")

