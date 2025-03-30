# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.routers import routers
from app.common.middlewares.exception import ExceptionMiddleware
from app.common.middlewares.headers import HeaderMiddleware
from app.common.middlewares.logging import LoggingMiddleware
from app.core.configs import AppConfig

# from app.core.lifespan import lifespan

app = FastAPI(
    title=AppConfig.APP_NAME,
    version=AppConfig.APP_VERSION,
    # lifespan=lifespan
)

# CORS 설정 추가 (프론트엔드와의 연동을 위해 필요)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

# app.add_exception_handler(Exception, GlobalExceptionHandler.handle)
app.add_middleware(ExceptionMiddleware)

app.add_middleware(HeaderMiddleware)
app.add_middleware(LoggingMiddleware)

app.include_router(router=routers)


@app.get("/")
async def health():
    return {"message": "Hello, FastAPI!"}
