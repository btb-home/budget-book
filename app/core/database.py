from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.configs import configs

engine = create_engine(configs.DATABASE_URL, pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
