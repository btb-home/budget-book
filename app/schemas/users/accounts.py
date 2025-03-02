from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.base import ReqBase, ResBase


class UserAccountBase(BaseModel):
    id: str = Field(..., title="User ID")
    name: str = Field(..., title="User Name")
    password: str = Field(None, exclude=True, title="User Password")

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