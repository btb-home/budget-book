from pydantic import BaseModel, Field
from typing import Generic, TypeVar
from datetime import datetime, timedelta

T = TypeVar("T")

from app.schemas.users.accounts import UserAccountBase
class SessionData(BaseModel, Generic[T]):
    user_info: T = Field(..., title="User Information")
    last_session_time: datetime = Field(..., title="Last Session Time")
    expire_time: timedelta = Field(..., title="Expire Time (minutes)")

    @staticmethod
    def create(user_info: BaseModel) -> "SessionData":
        return SessionData(
            user_info=user_info.model_dump(),
            last_session_time=datetime.now(),
            expire_time=timedelta(minutes=30),
        )

    def refresh(self):
        self.last_session_time = datetime.now()
    
    def update_user_info(self, user_info: T):
        self.user_info = user_info