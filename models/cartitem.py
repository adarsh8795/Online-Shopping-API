from db import db

class CartItem(db.Model):
    __tablename__ = "cartitem"
    id = db.Column(db.Integer,primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    
    # order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    

