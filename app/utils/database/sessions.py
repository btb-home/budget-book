from app.core.databases import redis_db
from app.core.configs import AppConfig
from uuid import uuid4


class SessionStorage:
    def __init__(self):
        self.client = redis_db

    def __getitem__(self, key):
        return self.client.get(key)

    def __setitem__(self, key, value):
        self.client.set(key, value)

    def __delitem__(self, key):
        self.client.delete(key)

    def generate_key(self) -> str:
        return f"session:{uuid4().hex}"

    def refresh(
        self, session_id: str, expire_min: int = AppConfig.SESSION_EXPIRE_MINUTES
    ):
        expire_sec = expire_min * 60
        self.client.expire(session_id, expire_sec)

    def get(self, key):
        return self[key]  # __getitem__ 호출

    def set(self, key, value):
        self[key] = value  # __setitem__ 호출
        