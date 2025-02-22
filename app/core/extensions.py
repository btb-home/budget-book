import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from app.core.configs import AppConfig
 
redis_app = redis.Redis(
    host=AppConfig.REDIS_HOST,
    port=AppConfig.REDIS_PORT,
    db=AppConfig.REDIS_DB_APP,
    password=AppConfig.REDIS_PASSWORD,
)

engine = create_engine(
    url=AppConfig.SQLALCHEMY_DATABASE_URL, 
    pool_recycle=3600,
    pool_pre_ping=True,
    poolclass=NullPool
)

aengine = create_async_engine(
    url=AppConfig.SQLALCHEMY_ASYNC_DATABASE_URL, 
    pool_recycle=3600,
    pool_pre_ping=True,
    poolclass=NullPool
)
