# utils/middlewares/sessions.py

from fastapi import Request, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from app.schemas.users.accounts import UserAccountRes
from app.schemas.users.sessions import SessionData
from app.utils.database.sessions import SessionStorage


def get_session_storage():
    """
    세션 저장소를 가져오는 함수.
    """
    session_storage = SessionStorage()
    yield session_storage


def get_session(
    request: Request,
    session_storage: SessionStorage = Depends(get_session_storage),
):
    """
    세션을 가져오는 함수.
    """
    session_id = request.cookies.get("session_id")
    session = session_storage.get(session_id)
    return session


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        사용자 세션 유효성을 확인하는 함수.
        """
        session: SessionData[UserAccountRes] = get_session(
            request, next(get_session_storage())
        )
        
        body = await request.body()
        # save_user_log(request, session, request_body)
        
        print(body)

        response = await call_next(request)

        return response
