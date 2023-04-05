from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Str(required = True)
    password = fields.Str(load_only = True)

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    
class PlainCategorySchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)

class CategorySchema(PlainCategorySchema,PlainItemSchema):
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))

class ItemSchema(PlainItemSchema):
    category_id = fields.Int(required = True)
    

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    category = fields.Str()

class SellerSchema(Schema):
    id=fields.Int(dump_only = True)
    name = fields.Str(required =True)
    email = fields.Str(required = True)
    password = fields.Str(load_only = True)
    
class UpdatedSellerSchema(SellerSchema):
    items = fields.List(fields.Nested(PlainItemSchema(),dump_only = True))

class SellerUpdateSchema(Schema):
    name = fields.Str(required =True)
    password = fields.Str(load_only =  True)

class DeliveryBoySchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)
    status = fields.Str(required = True)
    email = fields.Str(required=True)
    password = fields.Str(load_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)
    email = fields.Str(required = True)
    password = fields.Str(load_only =  True)
    

class UserUpdateSchema(Schema):
    name = fields.Str(required = True)
    password = fields.Str(load_only=  True)

class CartSchema(Schema):
    items = fields.List(fields.Nested(ItemSchema(),dump_only = True))
    value = fields.Float(dump_only = True)
    
class UserOrder(Schema):
    id =fields.Int(dump_only = True)

class OrderSchema(Schema):
   id = fields.Int(dump_only = True)
   delivery_address = fields.Str(required=True)
   order_value = fields.Float()
#    cart = fields.List(fields.Nested(UserOrder()),dump_only = True)
class CheckOrderSchema(OrderSchema):
    cart = fields.List(fields.Nested(UserOrder()),dump_only = True)


   