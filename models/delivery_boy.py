from db import db

class DeliverBoyModel(db.Model):
    __tablename__ = "deliveryboy"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(30),unique = False) 
    status = db.Column(db.String(30))
    email = db.Column(db.String(30) , unique= False)
    password = db.Column(db.String(30),nullable = False)
    order = db.relationship("OrderModel",back_populates ="deliveryboy", lazy = "dynamic")