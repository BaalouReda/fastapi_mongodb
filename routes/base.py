from routes import auth,product,user
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(user.router, prefix="/user", tags=["user"])