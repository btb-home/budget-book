from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.base import ReqBase, ResBase


class UserAccountBase(BaseModel):
    id: str = Field(..., title="ID")
    name: str = Field(..., title="이름")
    password: str = Field(None, exclude=True, title="비밀번호")
    
    admin_role_yn: Optional[bool] = Field(False, title="관리자 역할 여부")
    last_login_dttm: Optional[str] = Field(None, title="마지막 로그인 일시")
    last_login_ip: Optional[str] = Field(None, title="마지막 로그인 IP")

    def to_res(self) -> ResBase:
        # `model_dump`에서 `password`를 제외하고 None 값은 제외하여 반환
        res_data = self.model_dump()
        return UserAccountRes(**res_data)
    
class UserAccountRes(UserAccountBase, ResBase):
    password: Optional[str] = Field(None, title="User Password", exclude=True)

class UserAccountReq(UserAccountBase, ReqBase):
    password: str = Field(..., title="User Password")


class UserAccountUpdate(UserAccountBase):
    pass

# User Sign In
class UserSingIn(BaseModel):
    id: str = Field(..., title="User ID")
    password: str = Field(..., title="User Password")

class UserCheckIn(BaseModel):
    session_id: str = Field(..., title="Session ID")