import time
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.constants.headers import (
    X_CORRELATION_ID,
    X_FORWARDED_FOR,
    X_PROCESS_TIME,
)


class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Correlation-ID가 없으면 생성
        correlation_id = request.headers.get(X_CORRELATION_ID, str(uuid4()))
        request.state.correlation_id = correlation_id
        request.state.start_time = time.time()

        # 요청 처리
        response = await call_next(request)

        # 응답 헤더 설정
        process_time = f"{(time.time() - request.state.start_time):.3f} sec"
        response.headers[X_PROCESS_TIME] = process_time
        response.headers[X_CORRELATION_ID] = request.state.correlation_id

        return response
