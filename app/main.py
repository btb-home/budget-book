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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=AppConfig.APP_NAME, 
    version=AppConfig.APP_VERSION, 
    lifespan=lifespan
)

# CORS 설정 추가 (프론트엔드와의 연동을 위해 필요)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

app.add_exception_handler(ProjectException, ProjectErrorHandler.handle)
app.add_exception_handler(BusinessException, ClientErrorHandler.handle)
app.add_exception_handler(SQLAlchemyError, DatabaseErrorHandler.handle)
app.add_exception_handler(HTTPException, ClientErrorHandler.handle)
app.add_exception_handler(Exception, ServerErrorHandler.handle)

app.add_middleware(SessionMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(HeaderMiddleware)


app.include_router(router=api_router)

@app.get("/")
def main():
    return {"message": "Hello, FastAPI!"}

@app.get("/api")
def main2():
    return {"message": "Hello, FastAPI!"}