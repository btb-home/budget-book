#app/main.py

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.routers import api_router
from app.core.configs import AppConfig
from app.core.lifespan import lifespan
from app.utils.middlewares.exception import (
    ClientErrorHandler, DatabaseErrorHandler, ServerErrorHandler
)
app = FastAPI(
    title=AppConfig.APP_NAME,
    version=AppConfig.APP_VERSION,
    lifespan=lifespan
)

@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

app.add_exception_handler(SQLAlchemyError, DatabaseErrorHandler.handle)
app.add_exception_handler(HTTPException, ClientErrorHandler.handle)
app.add_exception_handler(Exception, ServerErrorHandler.handle)

app.include_router(router=api_router)