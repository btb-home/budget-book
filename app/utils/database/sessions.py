import json
from typing import Dict, Optional, Any
from uuid import uuid4
from datetime import datetime
from app.core.configs import AppConfig
from app.core.databases import redis_db
from app.schemas.users.sessions import UserSessionData
import pickle


class RedisSessionStorage:
    def __init__(self):
        self.client = redis_db  # Redis 클라이언트 초기화

    def __getitem__(self, key: str):
        """
        주어진 키로 Redis에서 데이터를 가져오는 메서드.
        """
        raw = self.client.get(key)  # Redis에서 키에 해당하는 데이터 조회
        return raw and pickle.loads(raw)  # 데이터를 반환

    def __setitem__(self, key: str, value: Any):
        """
        주어진 키로 Redis에 데이터를 저장하는 메서드.
        세션 만료 시간을 설정하여 저장.
        """
        pkl = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
        self.client.set(key, pkl, ex=AppConfig.SESSION_EXPIRE_MINUTES)  # 데이터를 Redis에 저장하고 만료 시간 설정

    def __delitem__(self, key: str):
        """
        주어진 키로 Redis에서 데이터를 삭제하는 메서드.
        """
        self.client.delete(key)  # Redis에서 키에 해당하는 데이터를 삭제

    def generate_session_id(self) -> str:
        """
        새 세션 ID를 생성하는 메서드.
        고유한 UUID를 생성하여 세션 ID 형식에 맞게 반환.
        """
        return f"session:{uuid4().hex}"  # 새 세션 ID를 생성하여 반환

    def refresh(self, session_id: str, session_data: UserSessionData, expire_min: int = AppConfig.SESSION_EXPIRE_MINUTES) -> None:
        """
        주어진 세션 ID와 데이터를 사용하여 세션 만료 시간을 갱신.
        """
        session_data.refresh()
        self[session_id] = session_data  # 세션 데이터를 Redis에 저장
        self.client.expire(session_id, expire_min * 60)  # 만료 시간 갱신