from fastapi import APIRouter, Path, Body
from fastapi.responses import Response

from app.schemas.systems.responses import SuccessResponse, GetOneResponse, GetListResponse
import app.services.commands.accounts as svc
import app.schemas.users.accounts as py_schema


router = APIRouter()


@router.post("/sign-in", response_model=SuccessResponse)
async def sign_in_account(
    user_signin_req: py_schema.UserSingIn = Body(...),
) -> Response:
    
    data = await svc.sign_in(user_signin_req)

    return GetOneResponse(
        data=data,
    )

@router.post("/sign-out", response_model=SuccessResponse)
async def sign_out_account(
    user_account_req: py_schema.UserAccountReq = Body(...),
) -> Response:
    
    data = await svc.create_account(user_account_req)

    return GetOneResponse(
        data=data,
    )
