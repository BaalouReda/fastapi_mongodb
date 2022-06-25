from fastapi import APIRouter,Depends,status,HTTPException
from models.utils import PyObjectId
from db import connect
from routes.verifyToken import verifyTokenAndAdmin,Token,verifyTokenAndAuthorization
from routes.auth import get_password_hash
from models.User import UserSchema
from datetime import datetime
from dateutil.relativedelta import relativedelta
router=APIRouter()

User=connect("User")

def serial_user(user: UserSchema) -> dict:
    return {
        "email": user["email"],
        "username": user["username"],
        "isAdmin": user["isAdmin"],
    }
# UPDATE
@router.put("/{user_id}")
def update_user(user_id:str,user:UserSchema=Depends(verifyTokenAndAuthorization)):
        try:
             hashed_password=get_password_hash(user.password)
             
             User.update_one({"_id":  PyObjectId(user_id)}, {"$set": {"email": user.email,"username":user.username,"password":hashed_password,
            "updatedAt":str(datetime.timestamp(datetime.now())) if user.updatedAt is None  else str(user.updatedAt) }})
             data = User.find_one({"_id":  PyObjectId(user_id)})
             updated_user: UserSchema = UserSchema(**data)
             return updated_user
        except Exception as e:
            print("ERROR: " + str(e))
            return None

# DELETE
@router.delete("/{user_id}",status_code=status.HTTP_200_OK)
def delete_user(user_id:str,token: Token=Depends(verifyTokenAndAuthorization)):
        try:
             User.delete_one({"_id": PyObjectId(user_id)})
             return {"message":"user is deleted"}
        except Exception as e:
            print("ERROR: " + str(e))
            return None

# GET USER
@router.get("/find/{user_id}",status_code=status.HTTP_200_OK)
def get_user(user_id:str,token: Token=Depends(verifyTokenAndAdmin)):
        try:
            data = User.find_one({"_id": PyObjectId(user_id)})
            _user: UserSchema = UserSchema(**data)
            return _user
        except Exception as e:
            print("ERROR: " + str(e))
            raise HTTPException(status_code=500, detail=str(e))

# GET ALL USER
@router.get("/findall",status_code=status.HTTP_200_OK)
def get_users(token: Token=Depends(verifyTokenAndAdmin)):
        try:
            users = User.find().sort({ "_id": -1 }).limit(5)
            return [serial_user(user) for user in users]
        except Exception as e:
            print("ERROR: " + str(e))
            raise HTTPException(status_code=500, detail=str(e))

# GET USER STATS
@router.get("/stats",status_code=status.HTTP_200_OK)
def get_stats(token: Token=Depends(verifyTokenAndAdmin)):
        last_year = datetime.datetime.timestamp(datetime. datetime. now()-relativedelta(years=1))
        try:
            users = User.aggregate([
      { "$match": { "createdAt": { "$gte": last_year } } },
      {
        "$project": {
          "month": { "$month": "$createdAt" },
        },
      },
      {
        "$group": {
          "_id": "$month",
          "total": { "$sum": 1 },
        },
      },
    ]);
            return [serial_user(user) for user in users]
        except Exception as e:
            print("ERROR: " + str(e))
            raise HTTPException(status_code=500, detail=str(e))

