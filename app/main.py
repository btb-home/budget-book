from fastapi import FastAPI
from app.api.routers import api_router
from app.core.configs import configs

app = FastAPI(
    title=configs.PROJECT_NAME,
)

@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

app.include_router(router=api_router)
