from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends,status,Request
from decouple import config
from models.User import UserSchema
from db import connect
from pydantic import BaseModel,EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    email: EmailStr | None = None

User=connect("User")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verifyToken(token:Token = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,config("SECRET_KEY"), algorithm=config("ALGORITHM"))
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    data = User.find_one({"email":token_data.email })
    if data is None:
        raise credentials_exception
    user: UserSchema = UserSchema(**data)
    return user

def verifyTokenAndAuthorization(user:UserSchema ,token:Token = Depends(oauth2_scheme)):
    user_existe=verifyToken(token=token)
    if user_existe.id == user.id or user_existe.isAdmin == True  :
        return True 
    else :
        return False
def verifyTokenAndAdmin(token: Token = Depends(oauth2_scheme)):
    user=verifyToken(token=token)
    if  user.isAdmin == True  :
        return True 
    else :
        return False