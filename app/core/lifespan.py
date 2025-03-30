# # app/core/lifespan.py

# import asyncio
# from contextlib import asynccontextmanager

# from fastapi import FastAPI

# from app.core.logger import LOGGER
# from app.services.init.database import init_database_data
# from app.services.init.redis import cleanup_redis, init_redis_data


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     LOGGER.info("=====================================")
#     LOGGER.info(f"[  App] ({app.title}:{app.version}) started")

#     try:
#         # 애플리케이션 시작 시 초기 데이터 로드
#         await init_redis_data()
#         await init_database_data()

#         yield
#     except (asyncio.CancelledError, KeyboardInterrupt) as e:
#         # 애플리케이션이 종료되었을 때의 예외 처리
#         LOGGER.info("[  App] System Cancelled")
#         raise KeyboardInterrupt(e)

#     finally:
#         # 애플리케이션 종료 시 정리 작업
#         await cleanup_redis()
#         LOGGER.info("[  App] Application Stopped")
#     LOGGER.info("=====================================")
