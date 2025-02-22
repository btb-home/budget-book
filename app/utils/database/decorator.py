from typing import Optional
from functools import wraps
from sqlalchemy.orm import Session

from app.utils.database.session import SessionMaker, db_session_context
from app.common.logging.logger import LOGGER


# 트랜잭션 데코레이터
def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db_session = db_session_context.get() or kwargs.get('session')

        if not db_session:
            db_session = _get_session(args)

        try:
            result = await func(*args, **kwargs)  # 비동기 함수 실행
            db_session.commit()

            LOGGER.info("Transaction is committed")

        except Exception as e:
            db_session.rollback()
            LOGGER.exception(f"Transaction is rollbacked: {e}")
            raise e

        finally:
            db_session.close()
            db_session_context.set(None)
            LOGGER.info("Session is closed")

        return result

    return wrapper


# 커넥션 관리 데코레이터
def connectional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_session = db_session_context.get()
        
        return func(*args, **kwargs, session=db_session)
    
    return wrapper

def _get_session(args):
    session = next((arg for arg in args if isinstance(arg, Session)), None)
    if session is None:
        raise ValueError("No Session object found in arguments")

    return session
