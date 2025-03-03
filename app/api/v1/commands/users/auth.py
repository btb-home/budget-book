# api/v1/commands/users/auth.py

from fastapi import APIRouter, Path, Body
from fastapi.responses import Response
from fastapi.requests import Request

from app.schemas.systems.responses import ActionResponse, SuccessResponse, GetOneResponse, GetListResponse
import app.services.commands.accounts as svc
import app.schemas.users.accounts as py_schema
import app.services.commands.clients_ip as client_svc
from app.utils.middlewares.sessions import set_session
from app.schemas.users.sessions import SessionData
from app.utils.middlewares.sessions import get_session_storage, SessionStorage
from fastapi import Depends

router = APIRouter()


@router.post("/sign-in", response_model=SuccessResponse)
async def sign_in_account(
    response: Response,
    session_storage: SessionStorage = Depends(get_session_storage),
    user_signin_req: py_schema.UserSignIn = Body(...),
) -> Response:
    user_info = await svc.auth(user_signin_req)

    session_data = SessionData.create(user_info)
    session_id = set_session(response, session_data, session_storage)

    return ActionResponse(
        data=user_info,
        message=f"세션 {session_id} 생성"
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
