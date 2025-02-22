import logging
from app.core.configs import AppConfig

logging.basicConfig(level=AppConfig.APP_LOG_LEVEL.value)

uvicorn_logger = logging.getLogger("uvicorn.error")
uvicorn_logger.setLevel(AppConfig.UVICORN_LOG_LEVEL.value)

app_logger = logging.getLogger("app")