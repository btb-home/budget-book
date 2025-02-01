from fastapi import FastAPI
from app.api.routers import api_router

app = FastAPI()

@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

app.include_router(router=api_router)
