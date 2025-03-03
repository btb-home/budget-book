# app/main.py

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.routers import api_router
from app.core.configs import AppConfig
from app.core.lifespan import lifespan
from app.utils.middlewares.exception import (
    ClientErrorHandler,
    DatabaseErrorHandler,
    ServerErrorHandler,
)
from app.utils.middlewares.headers import HeaderHandlingMiddleware
from app.utils.middlewares.logging import LoggingMiddleware
from app.utils.middlewares.sessions import SessionMiddleware
from app.common.exceptions.base import ProjectException

app = FastAPI(
    title=AppConfig.APP_NAME, 
    version=AppConfig.APP_VERSION, 
    lifespan=lifespan
)


@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

app.add_middleware(LoggingMiddleware)
app.add_middleware(HeaderHandlingMiddleware)
app.add_middleware(SessionMiddleware)

app.add_exception_handler(ProjectException, ClientErrorHandler.handle)
app.add_exception_handler(SQLAlchemyError, DatabaseErrorHandler.handle)
app.add_exception_handler(HTTPException, ClientErrorHandler.handle)
app.add_exception_handler(Exception, ServerErrorHandler.handle)

app.include_router(router=api_router)
