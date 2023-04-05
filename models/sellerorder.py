from db import db

class Sellerorder(db.Model):
    __tablename__ = "sellerorder"

    id = db.Column(db.Integer,primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))