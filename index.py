
from fastapi import FastAPI
import uvicorn
from decouple import config
from routes.base import api_router
app=FastAPI()

def include_router(app):
    app.include_router(api_router)
def start_application():
    app = FastAPI(title="FARM-ECOMMERCE", version="1.3.1")
    include_router(app)
    return app
app = start_application()
port=int(config("PORT"))
if __name__ == '__main__':
    uvicorn.run("index:app", port=port, reload=True, access_log=False)