import contextvars
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.extensions import aengine

AsyncSessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=aengine, class_=AsyncSession)
db_async_session_context = contextvars.ContextVar("async_session", default=None)
