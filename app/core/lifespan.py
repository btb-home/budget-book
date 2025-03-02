# app/core/lifespan.py

import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.services.init.redis import init_redis_data
from app.services.init.database import init_database
from app.core.logger import LOGGER

@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.info("=====================================")
    LOGGER.info(f"App({app.title}:{app.version}) started")

    try:
        # 애플리케이션 시작 시 초기 데이터 로드
        await init_redis_data()
        # await init_database()
        
        yield
    except (asyncio.CancelledError, KeyboardInterrupt) as e:
        # 애플리케이션이 종료되었을 때의 예외 처리
        LOGGER.info("App cancelled")
        raise KeyboardInterrupt(e)
        
    finally:
        # 애플리케이션 종료 시 정리 작업
        LOGGER.info("App stopped")
    LOGGER.info("=====================================")
