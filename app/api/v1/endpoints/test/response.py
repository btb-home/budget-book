from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response

from app.common.exceptions.biz import TestTeaPotException
from app.common.exceptions.sys import TestSysException
from app.schemas.systems.responses import (
    JSendError,
    JSendFailure,
    JSendResponse,
    JSendSuccess,
)

router = APIRouter()


@router.get("/health")
async def get_health_test() -> JSendResponse:

    return JSendSuccess(data={"status": "ok"})


@router.get("/normal")
async def get_normal_response_test() -> Response:

    return JSendSuccess(
        data={"status": "ok"},
    )


@router.get(
    "/client-error",
    status_code=status.HTTP_418_IM_A_TEAPOT,
    response_model=JSendFailure,
)
async def get_client_error_test() -> Response:
    """API-BKND-001 Get Module status"""

    raise TestTeaPotException("Test Exception")

    return JSendSuccess(
        data={"status": "ok"},
    )


@router.get(
    "/system-error",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    response_model=JSendError,
)
async def get_server_error_test() -> Response:
    """API-BKND-001 Get Module status"""

    raise TestSysException("Test Exception")

    return JSendSuccess(
        data={"status": "ok"},
    )


@router.get(
    "/server-error",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    response_model=JSendError,
)
async def get_server_error_test() -> Response:
    """API-BKND-001 Get Module status"""

    raise ValueError("Test Exception")

    return JSendSuccess(
        data={"status": "ok"},
    )
