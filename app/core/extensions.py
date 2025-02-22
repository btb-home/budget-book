import redis
from app.core.configs import AppConfig
 
redis_app = redis.Redis(
    host=AppConfig.REDIS_HOST,
    port=AppConfig.REDIS_PORT,
    db=AppConfig.REDIS_DB_APP,
    password=AppConfig.REDIS_PASSWORD,
)