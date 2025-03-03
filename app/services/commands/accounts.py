from app.services.commands.login_session import create_session, check_session
from app.models.users.accounts import UserAccount
from app.schemas.users.accounts import UserSignIn, UserAccountReq, UserCheckIn, UserAccountRes, UserAccountBase
from app.utils.database.decorator import transactional, connectional
from app.core.logger import LOGGER
from app.core.databases import redis_db
from app.utils.database.basic import select_one, insert
from sqlalchemy.orm.session import Session
import app.common.exceptions.business as biz_exc
import app.common.exceptions.data as db_exc

@connectional
async def auth(
    user_signin_req: UserSignIn,
    db_session: Session,
) -> bool:
    """
    사용자가 로그인할 때, 사용자 계정 정보를 데이터베이스에서 조회하여 인증.
    """
    data = select_one(db_session, UserAccount, UserAccountRes)(query={
        UserAccount.id.name: user_signin_req.id,
        UserAccount.password.name: user_signin_req.password.get_secret_value(),
    })

    if not data:
        raise biz_exc.UserAuthenticationFail(user_signin_req.id)

    res_data = data.to_res()
    LOGGER.info(f"[  API] User Account Fetched: {res_data.id}")
    
    return res_data


# 로그인 기능 (Sign-in)
@connectional
async def sign_in(
    user_signin_req: UserSignIn,
    db_session: Session,
) -> str:
    """
    사용자가 로그인할 때, 로그인 세션을 생성하고 토큰을 반환
    """
    data = select_one(db_session, UserAccount, UserAccountRes)(query={
        UserAccount.id.name: user_signin_req.id,
        UserAccount.password.name: user_signin_req.password.get_secret_value(),
    })

    if not data:
        raise Exception("User Account Not Found")

    res_data = data.to_res()
    LOGGER.info(f"User Account Fetched: {res_data}")

    # 세션 생성
    session_id = await create_session(res_data.model_dump())
    LOGGER.info(f"Generated session with ID: {session_id}")
    
    return session_id


# 로그아웃 기능 (Sign-out)
@transactional
async def sign_out(
    user_account_req: UserAccountReq,
    db_session: Session,
) -> UserAccountRes:
    """
    사용자가 로그아웃할 때, 사용자 계정 정보를 데이터베이스에 삽입 (업서트).
    """
    res = insert(db_session, UserAccount, UserAccountBase)(data=user_account_req, upsert=True)

    res_data = res.to_res()
    LOGGER.info(f"User Account Created: {res_data}")
    
    return res_data


# 세션 확인 기능 (Check-in)
async def check_in(
    user_check_in: UserCheckIn,
) -> dict:
    """
    세션 ID를 기반으로 Redis에서 세션을 조회하고, JWT 토큰을 디코딩하여 유효성 검사.
    """
    decoded_token = await check_session(user_check_in.session_id)
    LOGGER.info(f"Session Checked: {decoded_token}")
    
    cursor, keys = redis_db.scan(cursor=0, match='*', count=10)  # match로 필터링 가능
    cursor = 0
    print("==== Redis Keys and Values ====")

    while True:
        cursor, keys = redis_db.scan(cursor=cursor, match='session_*', count=10)
        
        for key in keys:
            # 키 출력
            key_str = key.decode('utf-8')
            print(f"Key: {key_str}")
            
            # 값 조회
            value = redis_db.get(key_str)  # 문자열 키의 경우 get 사용
            if value:
                value_str = value.decode('utf-8')
                print(f"Value: {value_str}")
            else:
                print(f"Value: None")
        
        if cursor == 0:  # cursor가 0으로 돌아오면 종료
            break
            
    print("==== Redis Keys and Values ====")
            
    return decoded_token
