#app/main.py

from fastapi import FastAPI
from app.api.routers import api_router
from app.core.configs import AppConfig

app = FastAPI(
    title=AppConfig.APP_NAME,
)

@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

app.include_router(router=api_router)
