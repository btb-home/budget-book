from typing import Any, Dict, Optional

from pydantic import BaseModel


class RequestLog(BaseModel):
    method: str
    endpoint: str
    headers: Dict[str, Any] | None
    client: str
    query_params: Dict[str, Any]
    path_params: Dict[str, Any]
    body: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class ResponseLog(BaseModel):
    status_code: int
    headers: Dict[str, Any]
    body: Optional[Dict[str, Any] | str] = None

    class Config:
        from_attributes = True


class LogRecord(BaseModel):
    x_correlation_id: str
    log_type: str
    endpoint: str
    request: Optional[Any]  # RequestInfo
    response: Optional[Any]  # ResponseInfo
    process_time_ms: str

    class Config:
        from_attributes = True
