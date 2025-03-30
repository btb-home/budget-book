from datetime import datetime, timedelta
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.core.configs import AppConfig
from app.schemas.users.accounts import UserAccountBase

# 제네릭 타입 T를 정의, UserSessionData의 user_info 타입에 사용
T = TypeVar("T")


class UserSessionData(BaseModel, Generic[T]):
    # 사용자 정보 (Generic 타입을 사용하여 다양한 타입을 받을 수 있음)
    user_info: T = Field(None, nullable=True, title="User Information")

    # 마지막 세션 시간 (사용자 세션 마지막 활동 시간)
    last_session_dttm: datetime = Field(..., title="Last Session Time")

    # 세션 만료 시간 (timedelta로 지정, 기본 단위는 분으로 설정)
    expire_time: timedelta = Field(..., title="Expire Time (minutes)")

    # 게스트 여부
    guest_yn: bool = Field(True, title="Guest User")

    # 정적 메서드로 새 UserSessionData 객체를 생성
    @staticmethod
    def create(user_info: BaseModel) -> "UserSessionData":
        """
        주어진 user_info로 새로운 UserSessionData 객체를 생성하고,
        마지막 세션 시간은 현재 시간으로 설정하며, 만료 시간은 설정된 세션 만료 시간을 사용.
        """
        return UserSessionData(
            user_info=user_info,
            last_session_dttm=datetime.now(),  # 현재 시간을 last_session_dttm에 저장
            expire_time=timedelta(
                minutes=AppConfig.SESSION_EXPIRE_MINUTES
            ),  # 설정된 SESSION_EXPIRE_MINUTES를 만료 시간으로 설정
            guest_yn=False,  # 게스트 여부를 False로 설정
        )

    @staticmethod
    def create_guest() -> "UserSessionData":
        """
        주어진 user_info로 새로운 UserSessionData 객체를 생성하고,
        마지막 세션 시간은 현재 시간으로 설정하며, 만료 시간은 설정된 세션 만료 시간을 사용.
        """
        return UserSessionData(
            last_session_dttm=datetime.now(),  # 현재 시간을 last_session_dttm에 저장
            expire_time=timedelta(
                minutes=AppConfig.SESSION_EXPIRE_MINUTES
            ),  # 설정된 SESSION_EXPIRE_MINUTES를 만료 시간으로 설정
            guest_yn=True,  # 게스트 여부를 True로 설정
        )

    # 세션 갱신 메서드 (마지막 세션 시간을 현재 시간으로 갱신)
    def refresh(self):
        """
        세션이 갱신되면, 마지막 세션 시간을 현재 시간으로 갱신
        """
        self.last_session_dttm = datetime.now()  # 현재 시간을 last_session_dttm에 저장

    # 사용자 정보를 갱신하는 메서드 (user_info 업데이트)
    def update_user_info(self, user_info: T):
        """
        새로운 사용자 정보를 세션에 업데이트
        """
        self.user_info = user_info  # user_info를 새로운 값으로 업데이트

    # 남은 만료 시간을 초 단위로 반환하는 메서드
    def get_remaining_time(self) -> int:
        """
        세션 만료 시간이 몇 초 남았는지를 계산하여 반환
        현재 시간과 마지막 세션 시간을 비교하여 남은 초를 계산
        """
        # 세션 만료 시간을 last_session_dttm에 더한 후, 현재 시간에서 빼서 남은 시간 계산
        remaining_time = (
            self.last_session_dttm + self.expire_time - datetime.now()
        ).total_seconds()
        return int(remaining_time)  # 남은 초를 반환
