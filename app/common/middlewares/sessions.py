import json
from uuid import uuid4

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.exceptions.business import (
    SessionException,
    SessionExpiredException,
    SessionGuestBannedException,
    SessionNotFoundException,
)
from app.common.middlewares.exception import ProjectErrorHandler
from app.core.configs import AppConfig
from app.core.logger import LOGGER
from app.schemas.users.sessions import UserSessionData
from app.services.middlewares.sessions import set_session
from app.utils.database.sessions import RedisSessionStorage


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        사용자의 세션 유효성을 확인하고,
        세션 정보를 바탕으로 접근 로그를 기록하는 미들웨어 함수.
        """
        # 1. 세션 정보 조회
        session_storage = RedisSessionStorage()
        session_id = request.cookies.get("session_id", "")
        if not session_id:
            # 게스트 세션 생성
            session_id = await self.create_guest_session_id(request, session_storage)

        LOGGER.info(f"세션 ID: {session_id}")

        # API 문서 페이지와 로그인 API는 세션 검사를 하지 않습니다.
        if self.is_signin_path(request.url.path):
            response = await call_next(request)

            return response

        if self.is_excluded_path(request.url.path):
            response = await call_next(request)
            response.set_cookie("session_id", session_id, httponly=True)

            return response

        try:
            session_data = await self.get_session_data(request, session_storage)
            # 게스트 사용자 차단
            if not session_data or session_data.guest_yn:
                raise SessionGuestBannedException(f"게스트 세션 ID: {session_id}")

            # 세션 만료 시간 체크
            remaining_time = session_data.get_remaining_time()
            if remaining_time <= 0:
                raise SessionExpiredException(f"세션 ID: {session_id}")
            LOGGER.info(
                f"세션({session_id}) 만료 시간은 {remaining_time}초 남았습니다."
            )

            # 세션 만료 시간 갱신
            session_storage.refresh(session_id, session_data)
            request.state.session = session_data

            response = await call_next(request)
            return response

        except SessionException as e:

            return await ProjectErrorHandler.handle(request, e)

    def is_signin_path(self, path: str) -> bool:
        """
        로그인 경로인지 확인하는 함수.
        """
        return path.endswith("/sign-in")

    def is_excluded_path(self, path: str) -> bool:
        """
        세션 검사를 제외할 경로를 체크하는 함수.
        """
        excluded_paths = ["/openapi.json", "/docs"]
        return any(path.endswith(excluded_path) for excluded_path in excluded_paths)

    async def get_session_data(
        self, request: Request, session_storage: RedisSessionStorage
    ) -> UserSessionData:
        """
        요청에서 세션을 추출하고 유효성 검사를 하는 함수.
        """
        session_id = request.cookies.get("session_id", "")
        session_data = session_storage[session_id]

        return session_data

    async def create_guest_session_id(
        self, request: Request, session_storage: RedisSessionStorage
    ) -> str:
        """
        비회원 세션을 생성하는 함수.
        """
        session_id = session_storage.generate_session_id()
        session_data = UserSessionData.create_guest()
        session_storage[session_id] = session_data
        request.cookies["session_id"] = session_id
        LOGGER.info(f"비회원 세션({session_id}) 생성")
        return session_id
