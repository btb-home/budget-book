from contextvars import ContextVar
from sqlalchemy.orm import sessionmaker
from app.core.extensions import engine

SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session_context = ContextVar("db_session", default=None)
