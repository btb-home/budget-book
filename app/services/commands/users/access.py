from fastapi import Request
from sqlalchemy.orm.session import Session

from app.core.databases import redis_db
from app.core.logger import LOGGER
from app.schemas.users.access import UserAccessLogReq
from app.schemas.users.sessions import UserSessionData
from app.services.commands.clients_ip import get_client_ip
from app.utils.database.basic import insert, select_one
from app.utils.database.decorator import transactional


# @transactional
async def save_access_log(
    request: Request,
    session: UserSessionData,
    request_body: bytes,
    # db_session: Session,
) -> bool:
    """
    사용자가 로그인할 때, 사용자 계정 정보를 데이터베이스에서 조회하여 인증.
    """
    if session:
        print(f"{session}, {type(session)}")

    if session and not str(request.url).endswith("/sign-in"):
        pass
        # user_log_req = UserAccessLogReq(
        #     user_id=session.user_info.id,
        #     user_name=session.user_info.name,
        #     client_ip=get_client_ip(request),
        #     method=request.method,
        #     request_url=request.url.components.path,
        #     request_body=request_body
        # )

        # print("============")
        # print(user_log_req)
        # print("============")
    else:
        print("============")
        print(f"세션 정보가 없습니다.")
        print("============")
