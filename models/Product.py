
from pydantic import BaseModel,Field
from typing import Optional
from models.utils import PyObjectId
from bson import ObjectId,Decimal128
import datetime

class ProductSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title : str
    desc :str
    img :str
    categories:list
    color:list
    inStock:Optional[bool]
    price:float
    createdAt:Optional[datetime.date]
    updatedAt:Optional[datetime.date]
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str,datetime.date:str,Decimal128:float}


