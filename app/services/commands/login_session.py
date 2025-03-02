import jwt
import datetime
from uuid import uuid4
from typing import Optional
from app.core.configs import AppConfig
from app.core.databases import redis_db
from fastapi import HTTPException, status

# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """JWT 토큰 생성"""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(hours=1))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AppConfig.SESSION_SECRET_KEY, algorithm=AppConfig.SESSION_ALGORITHM)
    return encoded_jwt


# 세션 관리: 로그인 (Sign-in)
async def create_session(user_signin_req: dict) -> str:
    """
    사용자가 로그인할 때, 사용자 정보를 확인하고 JWT 토큰을 생성하여 Redis에 저장.
    """
    session_id = f"session_id-{str(uuid4())}"
    access_token_data = {
        "sub": user_signin_req['id'],
        "name": user_signin_req['name'],
        "session_id": session_id
    }
    
    # JWT 토큰 생성
    access_token = create_access_token(access_token_data)
    
    # Redis에 세션 저장 (1시간 동안)
    redis_db.set(session_id, access_token, ex=3600)
    
    return session_id


from app.utils.middlewares.exception import SessionException
# 세션 관리: 세션 확인 (Check-in)
async def check_session(session_id: str) -> dict:
    """
    세션 ID를 기반으로 Redis에서 세션을 조회하고, JWT 토큰을 디코딩하여 유효성 검사.
    """
    session_data = redis_db.get(session_id)
    if session_data:
        session_data_str = session_data.decode('utf-8')

        try:
            decoded_token = jwt.decode(session_data_str, AppConfig.SESSION_SECRET_KEY, algorithms=[AppConfig.SESSION_ALGORITHM])
            return decoded_token

        except jwt.ExpiredSignatureError:
            # JWT 만료된 경우 401 Unauthorized 예외 발생
            raise SessionException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired"
            )

        except jwt.PyJWTError as e:
            # JWT 오류 발생 시 401 Unauthorized 예외 발생
            raise SessionException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid JWT token: {e}"
            )

    else:
        # 세션이 존재하지 않으면 401 Unauthorized 예외 발생
        raise SessionException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found"
        )
