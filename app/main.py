from fastapi import FastAPI
from app import models
from app.database import engine
from app.auth import routes as auth_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routes.router)

@app.get("/")
async def root():
    return {"message": "System's ON !!!"}

