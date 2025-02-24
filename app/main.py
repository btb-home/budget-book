#app/main.py

from fastapi import FastAPI
from app.api.routers import api_router
from app.core.configs import AppConfig
from app.core.lifespan import lifespan

app = FastAPI(
    title=AppConfig.APP_NAME,
    version=AppConfig.APP_VERSION,
    lifespan=lifespan
)

@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

app.include_router(router=api_router)