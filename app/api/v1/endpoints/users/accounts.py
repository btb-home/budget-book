from fastapi import APIRouter, Body, Path
from fastapi.responses import Response

import app.schemas.users.accounts as py_schema
import app.services.endpoints.users.accounts as svc
from app.schemas.systems.responses import (
    GetListResponse,
    GetOneResponse,
    SuccessResponse,
)

router = APIRouter()


@router.get("", response_model=GetListResponse)
async def get_account_list() -> Response:

    data = await svc.fetch_account_list()

    return GetListResponse(
        data=data,
    )


@router.post("", response_model=SuccessResponse)
async def create_account_info(
    user_account_req: py_schema.UserAccountReq = Body(...),
) -> Response:

    data = await svc.create_account(user_account_req)

    return GetOneResponse(
        data=data,
    )


@router.get("/{id}", response_model=SuccessResponse)
async def get_account_by_id(
    id: str = Path(...),
) -> Response:

    data = await svc.fetch_account_one(id)

    return GetOneResponse(
        data=data,
    )


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_account_by_id(
    id: str = Path(...),
) -> Response:

    data = []

    return SuccessResponse(
        data=data,
    )
