# app/main.py

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.routers import api_router
from app.core.configs import AppConfig
from app.core.lifespan import lifespan
from app.common.middlewares.exception import (
    ClientErrorHandler,
    DatabaseErrorHandler,
    ServerErrorHandler,
    ProjectErrorHandler
)
from app.common.middlewares.headers import HeaderMiddleware
from app.common.middlewares.logging import LoggingMiddleware
from app.common.middlewares.sessions import SessionMiddleware
from app.common.exceptions.base import ProjectException, BusinessException

app = FastAPI(
    title=AppConfig.APP_NAME, 
    version=AppConfig.APP_VERSION, 
    lifespan=lifespan
)

app.add_exception_handler(ProjectException, ProjectErrorHandler.handle)
# app.add_exception_handler(BusinessException, ClientErrorHandler.handle)
# app.add_exception_handler(SQLAlchemyError, DatabaseErrorHandler.handle)
# app.add_exception_handler(HTTPException, ClientErrorHandler.handle)
# app.add_exception_handler(Exception, ServerErrorHandler.handle)

app.add_middleware(SessionMiddleware)
# app.add_middleware(HeaderMiddleware)
# app.add_middleware(LoggingMiddleware)


app.include_router(router=api_router)

@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

@app.get("/api")
def main2():
    return {"message": "Hello, FastAPI!"}