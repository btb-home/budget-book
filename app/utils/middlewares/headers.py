from uuid import uuid4
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.commands.clients_ip import get_client_ip

class HeaderHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # X-Correlation-ID가 없으면 생성
        if "X-Correlation-ID" not in request.headers:
            request.headers._list.append((b"x-correlation-id", str(uuid4()).encode()))
        
        if "X-Forwarded-For" not in request.headers:
            request.headers._list.append((b"x-forwarded-for", get_client_ip(request).encode()))

        response = await call_next(request)
        return response
