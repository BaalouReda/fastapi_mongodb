
from turtle import color
from fastapi import APIRouter,Depends,status,HTTPException
from models.Product import ProductSchema
from models.utils import PyObjectId
from db import connect
from routes.verifyToken import verifyTokenAndAdmin,Token
import datetime

router=APIRouter()
Product=connect("Product")

def serial_product_update(product: ProductSchema) -> dict:
    return {
        "title": product["title"],
        "desc": product["desc"],
        "img": product["img"],
        "categories": product["categories"],
        "color": product["color"],
        "inStock": product["inStock"],
        "price": product["price"]
    }
# CREATE
@router.post("/")
def create_product( product:ProductSchema,token: Token):
    try:
            savedproduct= Product.insert_one({"title": product.title,"desc":product.desc,"img":product.img,
            "categories":product.categories,"color":product.color,"inStock":True,"price":product.price,
            "createdAt":str(datetime.timestamp(datetime.now())) if product.createdAt is None  else   str(product.createdAt),
            "updatedAt":str(datetime.timestamp(datetime.now())) if product.updatedAt is None  else str(product.updatedAt) })
            data = Product.find_one({"_id": savedproduct.inserted_id})
            created_product: ProductSchema = ProductSchema(**data)
            return created_product
            # print(created_user)
    except Exception as e:
            print("ERROR: " + str(e))
            return None

#UPDATE
@router.put("/{product_id}")
def update_product(product_id:str,product:ProductSchema,token: Token=Depends(verifyTokenAndAdmin)):
        try:
             Product.update_one({"_id":  PyObjectId(product_id)}, {"$set": dict(product)})
             data = Product.find_one({"_id":  PyObjectId(product_id)})
             created_product: ProductSchema = ProductSchema(**data)
             return created_product
        except Exception as e:
            print("ERROR: " + str(e))
            return None

# DELETE
@router.delete("/{product_id}",status_code=status.HTTP_200_OK)
def delete_product(product_id:str,token: Token=Depends(verifyTokenAndAdmin)):
        try:
             Product.delete_one({"_id": PyObjectId(product_id)})
             return {"message":"product is deleted"}
        except Exception as e:
            print("ERROR: " + str(e))
            return None

# GET PRODUCT
@router.get("/find/{product_id}",status_code=status.HTTP_200_OK)
def get_product(product_id:str):
        try:
            data = Product.find_one({"_id": PyObjectId(product_id)})
            created_product: ProductSchema = ProductSchema(**data)
            return created_product
        except Exception as e:
            print("ERROR: " + str(e))
            raise HTTPException(status_code=500, detail=str(e))

# GET ALL PRODUCTS
@router.get("/findall",status_code=status.HTTP_200_OK)
def get_product():
        try:
            products = Product.find()
            return [serial_product_update(product) for product in products]
        except Exception as e:
            print("ERROR: " + str(e))
            raise HTTPException(status_code=500, detail=str(e))
