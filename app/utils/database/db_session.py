# utils/database/session.py

from contextvars import ContextVar

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.core.databases import engine

# 동기 세션 메이커
SyncSessionMaker = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

# 세션 컨텍스트 변수
db_session_context = ContextVar("db_session", default=None)


def get_sync_session() -> Session:
    """
    동기 세션을 반환하는 함수입니다.
    """
    session = db_session_context.get()

    if session is None:
        session = SyncSessionMaker()  # 동기 세션
        db_session_context.set(session)

    return session


# =============
# 비동기 세션 메이커
# AsyncSessionMaker = sessionmaker(
#     bind=engine, class_=AsyncSession, expire_on_commit=False
# )

# def get_async_session() -> AsyncSession:
#     """
#     비동기 세션을 반환하는 함수입니다.
#     """
#     session = db_session_context.get()

#     if session is None:
#         session = AsyncSessionMaker()  # 비동기 세션
#         db_session_context.set(session)

#     return session

# @asynccontextmanager
# async def get_db_session_async() -> AsyncSession:
#     """
#     비동기 세션을 관리하는 컨텍스트 관리자.
#     """
#     db_session = AsyncSessionMaker()
#     try:
#         yield db_session
#     finally:
#         await db_session.close()
