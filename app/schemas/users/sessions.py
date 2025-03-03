from pydantic import BaseModel, Field
from typing import Generic, TypeVar
from datetime import datetime, timedelta

T = TypeVar("T")


class SessionData(BaseModel, Generic[T]):
    user_info: T = Field(..., title="User Information")
    last_session_time: datetime = Field(..., title="Last Session Time")
    expire_time: timedelta = Field(..., title="Expire Time (minutes)")

    @staticmethod
    def create(data):
        return SessionData(
            user_info=data,
            last_session_time=datetime.now(),
            expire_time=timedelta(minutes=30),
        )

    def refresh(self):
        self.last_session_time = datetime.now()
    
    def update_user_info(self, user_info: T):
        self.user_info = user_info