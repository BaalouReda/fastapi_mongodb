from datetime import date
from mongoengine import Document,StringField,IntField,DateTimeField,ObjectIdField
class OrderSchema(Document):
    userId = StringField(required=True,unique=True)
    productId=StringField()
    quantity=IntField(default=1)
    amount=IntField(required=True)
    address=ObjectIdField(required=True)
    status=StringField(default="pending")
    CreatedAt=DateTimeField(default=date.today()) 
    UpdatedAt= DateTimeField(default=date.today()) 


