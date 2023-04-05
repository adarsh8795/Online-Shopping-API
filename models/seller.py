from db import db


class SellerModel(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(80),unique = True,nullable = False)
    password = db.Column(db.String(80), unique = False, nullable = False)
    items = db.relationship("ItemModel", back_populates = "seller", lazy ="dynamic", cascade="all, delete" )
    order = db.relationship("OrderModel", back_populates = "seller", secondary = "sellerorder",lazy = "dynamic") 
    # order = db.relationship("OrderModel", back = "sellers")

 
    

    