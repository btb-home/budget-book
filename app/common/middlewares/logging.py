import json
import time
from uuid import uuid4

from fastapi import BackgroundTasks, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.constants.headers import X_CORRELATION_ID, X_PROCESS_TIME
from app.core.logger import LOGGER


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 응답 처리
        response = await call_next(request)

        # 응답 본문 읽기
        response_body = await self._capture_response_body(response)

        # Background Task로 로깅
        background_tasks = BackgroundTasks()
        background_tasks.add_task(
            self._log_request_response, request, response, response_body
        )
        response.background = background_tasks

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=response.headers,
            media_type=response.media_type,
            background=background_tasks,
        )

    async def _capture_response_body(self, response: Response) -> str:
        """응답 본문을 비동기적으로 읽어 반환"""
        response_body = b"".join([chunk async for chunk in response.body_iterator])

        # 비동기 이터레이터 복원
        async def _async_iter(data: bytes):
            yield data

        response.body_iterator = _async_iter(response_body)
        return response_body.decode() if response_body else ""

    async def _log_request_response(
        self,
        request: Request,
        response: Response,
        response_body: str,
    ):
        """요청 및 응답을 로깅"""
        request_body = await self._get_request_body(request)
        LOGGER.info(
            {
                "event": "application",
                "endpoint": request.url.path,
                "x_correlation_id": request.state.correlation_id,
                "process_time": response.headers[X_PROCESS_TIME],
                "request": {
                    "method": request.method,
                    "client": request.client.host,
                    "query_params": dict(request.query_params),
                    "path_params": request.path_params,
                    "body": self._shorten(request_body),
                },
                "response": {
                    "status_code": response.status_code,
                    "body": self._shorten(response_body),
                },
            }
        )

    async def _get_request_body(self, request: Request) -> dict | None:
        """요청 본문 추출"""
        try:
            if request.method in ["POST", "PUT", "PATCH"]:
                return await request.json()
        except json.JSONDecodeError:
            pass
        return None

    def _shorten(self, text: str, width: int = 100) -> str:
        from textwrap import shorten

        """요청 ID 생성"""
        text = text or ""
        placeholder = f"... {len(text) - width} more ..."

        return shorten(text, width, placeholder=placeholder)
