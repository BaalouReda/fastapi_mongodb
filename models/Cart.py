from datetime import date
from mongoengine import Document,StringField,IntField,DateTimeField
class CartSchema(Document):
    userId = StringField(required=True,unique=True)
    productId=StringField()
    quantity=IntField(default=1)
    CreatedAt=DateTimeField(default=date.today()) 
    UpdatedAt= DateTimeField(default=date.today()) 


