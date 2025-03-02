# utils/database/decorator.py

from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from app.utils.database.session import db_session_context, get_sync_session
from app.core.logger import LOGGER

# 트랜잭션 데코레이터
def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db_session = db_session_context.get()

        if not db_session:
            db_session = get_sync_session()
            db_session_context.set(db_session)

        try:
            result = await func(db_session=db_session, *args, **kwargs)
            db_session.commit()
            LOGGER.info("Transaction is committed")
        except SQLAlchemyError as e:
            if db_session:
                db_session.rollback()
                LOGGER.info(f"Transaction is rollbacked - {e}")
            raise
        except Exception as e:
            if db_session:
                db_session.rollback()
                LOGGER.exception(f"Transaction is rollbacked - {e}")
            raise
        finally:
            if db_session:
                db_session.close()
            db_session_context.set(None)
            LOGGER.info("Session is closed")

        return result

    return wrapper

# 커넥션 관리 데코레이터
def connectional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db_session = db_session_context.get()

        if not db_session:
            db_session = get_sync_session()
            db_session_context.set(db_session)
        
        return await func(db_session=db_session, *args, **kwargs)
    return wrapper
