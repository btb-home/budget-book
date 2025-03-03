from fastapi import Request, Response, Depends
from app.schemas.users.sessions import UserSessionData
from app.utils.database.sessions import RedisSessionStorage
from app.core.logger import LOGGER
from typing import Generator

def get_session_storage() -> Generator:
    """
    세션 저장소 인스턴스를 반환하는 함수.
    """
    storage = RedisSessionStorage()
    yield storage

def get_session_data(request: Request, session_storage: RedisSessionStorage = Depends(get_session_storage)) -> UserSessionData:
    """
    요청에서 세션 데이터를 가져오는 함수.
    """
    session_id = request.cookies.get("session_id", "")
    session_data = session_storage[session_id]
    if not session_data:
        raise ValueError("세션이 존재하지 않습니다.")
    return session_data

def get_session_id(request: Request) -> str:
    """
    요청에서 세션 ID를 가져오는 함수.
    """
    session_id = request.cookies.get("session_id", "")
    return session_id

def set_session(response: Response, session_data: UserSessionData, session_storage: RedisSessionStorage, session_id: str = None) -> str:
    """
    세션을 설정하고 쿠키에 세션 ID를 저장하는 함수.
    세션을 설정한 후, 세션 만료 시간을 갱신.
    """
    # 세션 ID가 없거나, 만료된 세션인 경우 새로 생성
    remaining_time = session_data.get_remaining_time()
    if not session_id or remaining_time <= 0:
        session_id = session_storage.generate_session_id()
    
    # 세션 데이터를 저장
    session_storage[session_id] = session_data
        
    # 세션 만료 시간을 갱신
    session_storage.refresh(session_id, session_data)

    # 응답에 쿠키로 세션 ID 추가
    response.set_cookie("session_id", session_id, httponly=True)
    LOGGER.info(f"[  Sys] Session 설정: {session_id}. Guest: {session_data.guest_yn}")
    
    return session_id

def delete_session(response: Response, session_id: str, session_storage: RedisSessionStorage) -> None:
    """
    세션을 삭제하는 함수.
    """
    del session_storage[session_id]
    response.delete_cookie(key="session_id")
    
    LOGGER.info(f"[  Sys] Session 삭제: {session_id}")
