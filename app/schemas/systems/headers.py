from uuid import uuid4

from fastapi import Header
from pydantic import BaseModel

class YabasCommonHeader(BaseModel):
    """Common header class"""

    x_forwarded_for: str | None = Header(
        alias="X-Forwarded-For",
        default_factory=lambda: "0.0.0.0",
    )
    x_service_id: str | None = Header(
        alias="X-Service-ID",
        default=None,  # yabas-bknd
    )
    x_correlation_id: str | None = Header(
        alias="X-Correlation-ID",
        default_factory=lambda: str(uuid4()), 
    )
    x_user_id: str | None = Header(
        alias="X-User-ID",
        default=None,
    )
