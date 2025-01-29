from fastapi import FastAPI
from long_task_routes import router as long_tasks_router
from nnunet_dataset_routes import router as ds_router

app = FastAPI()

app.include_router(long_tasks_router)
app.include_router(ds_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Celery example!"}
