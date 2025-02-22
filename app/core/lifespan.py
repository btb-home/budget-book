# app/core/lifespan.py

import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.services.init.redis import init_redis_data
from app.common.logging.logger import LOGGER

from app.core.extensions import redis_app
@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.info("=====================================")
    LOGGER.info(f"App({app.title}:{app.version}) started")
    
    try:
        # 애플리케이션 시작 시 초기 데이터 로드
        await init_redis_data()
        
        from app.models.base import BaseModel
        from app.core.extensions import engine
        BaseModel.metadata.create_all(bind=engine)

        yield
    except asyncio.CancelledError:
        # 애플리케이션이 종료되었을 때의 예외 처리
        LOGGER.info("App cancelled")
        
    finally:
        # 애플리케이션 종료 시 정리 작업
        LOGGER.info("App stopped")


