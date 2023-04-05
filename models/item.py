from db import db
from models import SellerModel


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    price = db.Column(db.Float(precision = 2))
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"))
    seller = db.relationship("SellerModel", back_populates = "items")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id") )
    category = db.relationship("CategoryModel", back_populates="items")
    customer = db.relationship("CustomerModel" ,back_populates ="cart", secondary = "cartitem",lazy = "dynamic")


    # category_id = db.Column(db.Integer, db.ForeignKey("category.id")
    # seller_id = db.Column(db.Integer,db.ForeignKey("sellers.id") ,unique = False, nullable = False)
    # seller = db.relationship("SellerModel", back_populates = "items")
    # category = db.relationship("CategoryModel", back_populates = "items")