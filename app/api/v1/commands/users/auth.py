# # api/v1/commands/users/auth.py

# from fastapi import APIRouter, Body, Depends, Request
# from fastapi.responses import Response

# import app.schemas.users.accounts as py_schema
# import app.services.commands.accounts as svc
# from app.core.logger import LOGGER
# from app.schemas.systems.responses import (
#     GetListResponse,
#     GetOneResponse,
#     SuccessResponse,
# )
# from app.schemas.users.sessions import UserSessionData
# from app.services.middlewares.sessions import (
#     RedisSessionStorage,
#     delete_session,
#     get_session_data,
#     get_session_id,
#     get_session_storage,
#     set_session,
# )

# router = APIRouter()


# @router.post("/sign-in", response_model=SuccessResponse)
# async def sign_in_account(
#     response: Response,
#     session_id: str = Depends(get_session_id),
#     session_storage: RedisSessionStorage = Depends(get_session_storage),
#     user_signin_req: py_schema.UserSignIn = Body(...),
# ) -> Response:
#     try:
#         user_res = await svc.auth(user_signin_req)

#         session_data = UserSessionData.create(user_res)
#         session_id = set_session(response, session_data, session_storage, session_id)

#         response.set_cookie("session_id", session_id, httponly=True)
#         LOGGER.info(f"[  App] User({user_res.id}) - 세션 {session_id} 생성")

#         return ActionResponse(message=f"로그인 성공")
#     except Exception as e:
#         LOGGER.error(f"[  App] 로그인 실패: {e}")

#         response.set_cookie("session_id", session_id, httponly=True)
#         session_data = UserSessionData.create_guest()
#         session_id = set_session(response, session_data, session_storage, session_id)

#         return ActionResponse(
#             status="failure", status_code=400, code=400, message=f"로그인 실패: {e}"
#         )


# @router.post("/sign-out", response_model=None)
# async def sign_out_account(
#     request: Request,
#     response: Response,
#     session_id: str = Depends(get_session_id),
#     session_storage: RedisSessionStorage = Depends(get_session_storage),
# ) -> Response:

#     delete_session(response, session_id, session_storage)

#     return ActionResponse(message="로그아웃 성공")


# @router.post("/check-in", response_model=SuccessResponse)
# async def sign_in_account(
#     session_id: str = Depends(get_session_id),
#     session_storage: RedisSessionStorage = Depends(get_session_storage),
# ) -> Response:

#     data = session_storage[session_id]

#     return ActionResponse(message=f"세션 데이터({session_id})")
