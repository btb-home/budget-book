# api/v1/commands/users/auth.py

from fastapi import APIRouter, Path, Body
from fastapi.responses import Response
from fastapi.requests import Request

from app.schemas.systems.responses import ActionResponse, SuccessResponse, GetOneResponse, GetListResponse
import app.services.commands.accounts as svc
import app.schemas.users.accounts as py_schema
import app.services.commands.clients_ip as client_svc

router = APIRouter()


@router.post("/sign-in", response_model=SuccessResponse)
async def sign_in_account(
    request: Request,
    user_signin_req: py_schema.UserSignIn = Body(...),
) -> Response:
    data = await svc.auth(user_signin_req)

    data = await svc.sign_in(user_signin_req)

    return ActionResponse(
        message=data,
    )

@router.post("/sign-out", response_model=SuccessResponse)
async def sign_out_account(
    user_account_req: py_schema.UserAccountReq = Body(...),
) -> Response:
    
    data = await svc.sign_out(user_account_req)

    return GetOneResponse(
        data=data,
    )

@router.post("/check-in", response_model=SuccessResponse)
async def sign_in_account(
    user_check_in: py_schema.UserCheckIn = Body(...),
) -> Response:
    
    data = await svc.check_in(user_check_in)
          
    return ActionResponse(
        data=data
    )
