import os
from enum import Enum
from app.common.configs.configs import Setting

setting = Setting.load_env()

class AppConfig(Enum):
    """config for the app

    """
    APP_NAME = os.getenv("APP_NAME")
    APP_VERSION = os.getenv("APP_VERSION")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION")
    APP_DEBUG = os.getenv("APP_DEBUG")

    APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL")
    
    UVICORN_LOG_LEVEL = os.getenv("UVICORN_LOG_LEVEL")
