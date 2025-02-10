from fastapi import FastAPI
from nnunet_dataset_routes import router as dataset_router

app = FastAPI()

app.include_router(dataset_router)


@app.get("/ping")
async def ping():
    return {"msg": "Pong"}

@app.get("/")
async def root():
    return {"msg": "Welcome to the FastAPI Celery example 2!"}
