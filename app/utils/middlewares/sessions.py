# utils/middlewares/sessions.py

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class SessionValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def handle(self, request: Request) -> bool:
        """
        사용자 세션 유효성을 확인하는 함수.
        """
        session_token = request.headers.get("Authorization")
        if not session_token or not self.validate_session(session_token):
            return False
        return True

    def validate_session(self, token: str) -> bool:
        """
        세션 검증 로직.
        """
        # 여기에 실제 세션 검증 로직 추가
        # 예: 데이터베이스 조회 또는 캐시 검증
        return token == "valid-session-token"

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        미들웨어의 메인 실행 함수.
        """
        if not await self.handle(request):
            raise HTTPException(status_code=401, detail="Invalid or missing session token")
        
        response = await call_next(request)
        return response
