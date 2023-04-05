from db import db

class CustomerOrderModel(db.Model):
    __tablename__ = "customerorder"
    id = db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey("customers.id"))
    order_id= db.Column(db.Integer,db.ForeignKey("orders.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    seller_id= db.Column(db.Integer, db.ForeignKey("sellers.id"))