from db import db

class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),unique = True) 
    items = db.relationship("ItemModel", back_populates ="category", lazy = "dynamic")

# from db import db 
# class ItemCategory(db.Model):
#     __tablename__ = "itemcategory"
#     id = db.Column(db.Integer,primary_key = True)
#     category_id = db.Column(db.Integer,db.ForeignKey("category.id"))
#     item_id = db.Column(db.Integer,db.ForeignKey("items.id"))

