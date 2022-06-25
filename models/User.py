
from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from models.utils import PyObjectId
from bson import ObjectId
import datetime
class UserSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email : EmailStr
    username :str
    password :str
    isAdmin: Optional[bool]=False
    img:Optional[str]
    createdAt:Optional[datetime.date]
    updatedAt:Optional[datetime.date]
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str,datetime.date:str}


