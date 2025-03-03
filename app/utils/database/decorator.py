# utils/database/decorator.py

from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from app.utils.database.db_session import db_session_context, get_sync_session
from app.core.logger import LOGGER
import base64
from uuid import uuid4

def generate_short_id() -> str:
    # UUID를 생성하고 Base64로 인코딩한 후, URL-safe한 base62로 변환
    id_bytes = uuid4().bytes
    return base64.urlsafe_b64encode(id_bytes).decode("utf-8").rstrip("=")[:6]

# 트랜잭션 데코레이터
def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db_session = db_session_context.get()

        if not db_session:
            db_session = get_sync_session()
            db_session_context.set(db_session)
        
        # db_session_id 생성
        db_session_id = generate_short_id()

        # db_session에 db_session_id를 저장
        db_session.db_session_id = db_session_id

        try:
            result = await func(db_session=db_session, *args, **kwargs)

            db_session.commit()

            commit_count = len(db_session.new)
            LOGGER.info(f"[   DB] ({db_session_id}) 트랜잭션이 {commit_count}건 커밋되었습니다.")
        except SQLAlchemyError as e:
            if db_session:
                db_session.rollback()
                LOGGER.info(f"[   DB] ({db_session_id}) 트랜잭션 롤백됨 - 오류: {e}")
            raise
        except Exception as e:
            if db_session:
                db_session.rollback()
                LOGGER.exception(f"[   DB] ({db_session_id}) 트랜잭션 롤백됨 - 오류: {e}")
            raise
        finally:
            if db_session:
                db_session.close()
            db_session_context.set(None)
            LOGGER.info(f"[   DB] ({db_session_id}) 세션이 종료되었습니다.")

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

        # db_session_id 생성
        db_session_id = generate_short_id()

        # db_session에 db_session_id를 저장
        db_session.db_session_id = db_session_id
                
        return await func(db_session=db_session, *args, **kwargs)

    return wrapper
