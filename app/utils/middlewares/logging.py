import json
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import LOGGER
from app.schemas.systems.logs import LogRecord, RequestLog, ResponseLog

class LoggingMiddleware(BaseHTTPMiddleware):
    LOG_LEVELS = {4: LOGGER.warning, 5: LOGGER.error}

    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/api"):
            return await call_next(request)

        start_time = time.time()
        x_correlation_id = request.headers.get("X-Correlation-ID")

        # 요청 정보를 수집하면서 민감한 정보 마스킹 처리
        request_info = await self._collect_request_info(request)
        response = await call_next(request)
        response_info = await self._collect_response_info(response)

        process_time = self._calculate_process_time(start_time)
        log_record = self._log_request_response(x_correlation_id, request.url.path, request_info, response_info, process_time)

        log_func = self._get_log_function(response.status_code)
        log_func(f"[  API] {json.dumps(log_record, ensure_ascii=False)}")

        return response

    async def _collect_request_info(self, request: Request) -> RequestLog:
        try:
            # POST, PUT, PATCH 요청에서 body를 받아옴
            request_body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
        except json.JSONDecodeError:
            request_body = None

        return RequestLog(
            method=request.method,
            endpoint=str(request.url.path),
            headers=dict(request.headers),
            client=request.client.host,
            query_params=dict(request.query_params),
            path_params=dict(request.path_params),
            body=request_body,
        )

    async def _collect_response_info(self, response: Response) -> ResponseLog:
        response_body = getattr(response, "body", b"").decode() or None

        return ResponseLog(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response_body,
        )
    
    def _get_log_function(self, status_code: int):
        first_digit = status_code // 100
        return self.LOG_LEVELS.get(first_digit, LOGGER.info)

    def _log_request_response(self, x_correlation_id: str, endpoint: str, request_info: RequestLog, response_info: ResponseLog, process_time: str) -> LogRecord:
        return LogRecord(
            x_correlation_id=x_correlation_id,
            log_type="application",
            endpoint=endpoint,
            request=request_info.model_dump(exclude={"headers"}),  # headers 제외, body 제외
            response=response_info.model_dump(exclude={"headers"}),  # headers 제외
            process_time_ms=process_time,
        ).model_dump()
        
    def _calculate_process_time(self, start_time: float) -> str:
        return f"{(time.time() - start_time) * 1000:.3f} ms"
