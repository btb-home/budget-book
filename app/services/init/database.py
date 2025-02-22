from app.models.base import BaseModel
from app.core.databases import engine
from app.common.logging.logger import LOGGER

async def init_database():
    BaseModel.metadata.create_all(bind=engine)
    LOGGER.info("Database initialized")
    