from contextvars import ContextVar
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.core.databases import engine

SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session_context = ContextVar("db_session", default=None)

def get_session():
    session = db_session_context.get()
    
    if session is None:
        session = SessionMaker()
        db_session_context.set(session)
        
    return session
