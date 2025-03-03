# utils/middlewares/sessions.py

from typing import Any
from fastapi import Request, Depends, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.schemas.users.accounts import UserAccountRes
from app.schemas.users.sessions import SessionData
from app.utils.database.sessions import SessionStorage
from app.services.commands.users.access import save_access_log
from app.core.logger import LOGGER

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
    session_id = request.cookies.get("session_id", "")
    session = session_storage.get(session_id)
    return session

def set_session(response: Response, session: SessionData, session_storage: SessionStorage, session_id=None) -> str:
    """
    세션을 설정하는 함수.
    """
    
    session_id = session_id if session_id else session_storage.generate_session_id()
    session_storage.set(session_id, session.model_dump_json())
    response.set_cookie("session_id", session_id, httponly=True)

    LOGGER.info(f"Session set: {session_id}")

    return session_id


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        사용자 세션 유효성을 확인하는 함수.
        """
        session: SessionData[UserAccountRes] = get_session(
            request, next(get_session_storage())
        )
        
        body = await request.body()
        save_access_log(request, session, body)

        response = await call_next(request)

        return response
