from typing import Optional
from functools import wraps
from sqlalchemy.orm import Session

from app.utils.database.session import SessionMaker, db_session_context
from app.common.logging.logger import LOGGER


# 트랜잭션 데코레이터
def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_session = db_session_context.get()

        # 새로운 세션 생성 여부 플래그
        is_new_session = db_session is None
        if is_new_session:
            db_session = SessionMaker()
            db_session_context.set(db_session)

        try:
            result = func(*args, **kwargs)  # 비동기 함수 실행
            if is_new_session:
                db_session.commit()

        except Exception as e:
            if is_new_session:
                db_session.rollback()
            raise e

        finally:
            if is_new_session:
                db_session.close()
                db_session_context.set(None)

        return result

    return wrapper


# 커넥션 관리 데코레이터
def connectional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_session = db_session_context.get()
        
        return func(*args, **kwargs, session=db_session)
    
    return wrapper
