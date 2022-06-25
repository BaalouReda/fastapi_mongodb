
from pymongo import MongoClient
from decouple import config
def connect(collection_Name) -> MongoClient:
    mongodb_url = f'mongodb+srv://{config("MONGO_USER")}:{config("MONGO_PASSWORD")}@cluster0.ifkr2.mongodb.net/{config("MONGO_DB_NAME")}?retryWrites=true&w=majority'
    mongodb_name=config("MONGO_DB_NAME")
    try:
        client = MongoClient(mongodb_url)
        assert client is not None
        print(f"Connected to MongoDB at {mongodb_url}")
        db = client[f"{mongodb_name}"]
        collection = db[collection_Name]
        return collection

    except Exception as e:
        print("ERROR: " + str(e))
        return None
connect("User")
