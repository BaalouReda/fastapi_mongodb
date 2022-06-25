
from fastapi import APIRouter,HTTPException
from sqlalchemy import null
from models.User import UserSchema
from passlib.context import CryptContext
from db import connect
from datetime import datetime, timedelta 
from jose import jwt
from decouple import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router=APIRouter()

User=connect("User")
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 

# function that create token using jwt :
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,config("SECRET_KEY"), algorithm=config("ALGORITHM"))
    return encoded_jwt  

@router.post("/register")
def  register(user:UserSchema):
    user_existe = User.find_one({"email": user.email})
    if user_existe is None :
        hashed_password=get_password_hash(user.password)
        try:
            # newuser: UserSchema = UserSchema(**user)
            #saveduser= User.insert_one(dict(user))
            saveduser= User.insert_one({"email": user.email,"username":user.username,"password":hashed_password,
            "isAdmin": False,
            "img":user.img,
            "createdAt":str(datetime.timestamp(datetime.now())) if user.createdAt is None  else   str(user.createdAt),
            "updatedAt":str(datetime.timestamp(datetime.now())) if user.updatedAt is None  else str(user.updatedAt) })
            data = User.find_one({"_id": saveduser.inserted_id})
            created_user: UserSchema = UserSchema(**data)
            return created_user
            # print(created_user)
        except Exception as e:
            print("ERROR: " + str(e))
            return None
    else :
        raise HTTPException(status_code=400, detail="Email already registered")

@router.get("/login")
def login(user:UserSchema):  
    data = User.find_one({"email": user.email,"username":user.username})
    
    if data is not None :
        user_existe: UserSchema = UserSchema(**data)
        if not verify_password(user.password,user_existe.password) :
            raise HTTPException(status_code=400, detail="Wrong credentials!")
        else :
            access_token_expires = timedelta(minutes=int(config("ACCESS_TOKEN_EXPIRE_MINUTES")))
            access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
    else :
        raise HTTPException(status_code=400, detail="Wrong credentials!")      

