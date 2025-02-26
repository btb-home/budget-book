from typing import Optional
from functools import wraps
from sqlalchemy.orm import Session

from app.utils.database.session import SessionMaker, db_session_context
from app.core.logger import LOGGER


# 트랜잭션 데코레이터
def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db_session = db_session_context.get() or kwargs.get('db_session')

        if not db_session:
            db_session = _get_session(args)
            db_session_context.set(db_session)

        try:
            result = await func(*args, db_session=db_session, **kwargs)  # 비동기 함수 실행
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
        
        return func(*args, session=db_session, **kwargs)
    
    return wrapper

def _get_session(args):
    # `args`에서 `Session` 타입 객체를 검색
    session = next((arg for arg in args if isinstance(arg, Session)), None)

    # 세션이 없으면 기본 세션 컨텍스트를 시도
    if session is None:
        session = db_session_context.get()

    # 여전히 세션이 없으면 오류 발생
    if session is None:
        from app.utils.database.session import get_session
        session = get_session()
    #     raise ValueError("No Session object found in arguments or ContextVar")

    return session
