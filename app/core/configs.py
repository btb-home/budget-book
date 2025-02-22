import os
from enum import Enum
from app.common.configs.configs import Setting

setting = Setting.load_env()

class AppConfig:
    """config for the app

    """
    APP_NAME: str = os.environ["APP_NAME"]
    APP_VERSION: str = os.environ["APP_VERSION"]
    APP_ENVIRONMENT: str = os.environ["APP_ENVIRONMENT"]

    APP_LOG_LEVEL: str = os.environ["APP_LOG_LEVEL"]
    
    UVICORN_LOG_LEVEL: str = os.environ["UVICORN_LOG_LEVEL"]
    
    REDIS_HOST: str = os.environ["REDIS_HOST"]
    REDIS_PORT: int = int(os.environ["REDIS_PORT"])
    REDIS_DB_SESSION: int = int(os.environ["REDIS_DB_SESSION"])
    REDIS_DB_HISTORY: int = int(os.environ["REDIS_DB_HISTORY"])
    REDIS_DB_APP: int = int(os.environ["REDIS_DB_APP"])
    REDIS_PASSWORD: str = os.environ["REDIS_PASSWORD"]
