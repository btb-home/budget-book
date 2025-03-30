import json
import time
from uuid import uuid4
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import AsyncIterator
from app.core.logger import LOGGER
from app.schemas.systems.logs import LogRecord, RequestLog, ResponseLog
from app.common.constants.headers import X_CORRELATION_ID, X_PROCESS_TIME

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get(X_CORRELATION_ID, uuid4().hex)
        start_time = time.time()
        request.state.correlation_id = correlation_id

        response: Response = await call_next(request)
        response.headers[X_CORRELATION_ID] = correlation_id
        response.headers[X_PROCESS_TIME] = f"{time.time() - start_time:.4f} sec"

        log_record = await self._log_request_response(request, response)
        LOGGER.info(json.dumps(log_record, ensure_ascii=False))

        return response

    async def _log_request_response(self, request: Request, response: Response) -> dict:
        request_body = await self._get_request_body(request)
        response_body = await self._get_response_body(response)

        return LogRecord(
            event="application",
            endpoint=request.url.path,
            x_correlation_id=response.headers[X_CORRELATION_ID],
            process_time_ms=response.headers[X_PROCESS_TIME],
            request=RequestLog(
                method=request.method,
                endpoint=request.url.path,
                headers=None,  # 헤더 제외
                client=request.client.host,
                query_params=request.query_params,
                path_params=request.path_params,
                body=request_body,
            ).model_dump(),
            response=ResponseLog(
                status_code=response.status_code,
                body=response_body,
            ).model_dump(),
        ).model_dump()


    async def _get_request_body(self, request: Request) -> dict | None:
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                return await request.json()
            except json.JSONDecodeError:
                pass
        return None


    async def _get_response_body(self, response: Response) -> str | None:
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # 비동기 이터레이터 복원
        async def _async_iter(data: bytes) -> AsyncIterator[bytes]:
            yield data

        response.body_iterator = _async_iter(response_body)
        return response_body.decode() if response_body else None
