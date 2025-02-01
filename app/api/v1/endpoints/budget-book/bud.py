from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response

from app.schemas.systems.responses import SuccessResponse, GetOneResponse, FailureResponse, ErrorResponse

router = APIRouter()


@router.get("/normal", response_model=GetOneResponse)
async def get_normal_response_test() -> Response:

    data = {"status": "ok"}

    return SuccessResponse(
        data=data,
    )


@router.get("/client-error", status_code=status.HTTP_418_IM_A_TEAPOT, response_model=FailureResponse)
async def get_client_error_test() -> Response:
    """API-BKND-001 Get Module status"""

    raise HTTPException(418, "Test Exception")


@router.get("/server-error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, response_model=ErrorResponse)
async def get_server_error_test() -> Response:
    """API-BKND-001 Get Module status"""

    raise Exception("Test Exception")
