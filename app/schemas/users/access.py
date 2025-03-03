from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, SecretStr
from app.schemas.base import ReqBase, ResBase


class UserAccessLogBase(BaseModel):
    user_id: str = Field(..., title="사용자 ID")
    user_name: str = Field(..., title="사용자 이름")
    
    client_ip: str = Field(..., title="클라이언트 IP")
    request_method_type: str = Field(..., title="요청 메소드 타입")
    request_url: str = Field(..., title="요청 URL")
    request_body: Dict[str, Any] = Field({}, title="요청 바디")

    def to_res(self) -> ResBase:
        # `model_dump`에서 `password`를 제외하고 None 값은 제외하여 반환
        res_data = self.model_dump()
        return UserAccessLogRes(**res_data)


    
class UserAccessLogRes(UserAccessLogBase, ResBase):
    pass

class UserAccessLogReq(UserAccessLogBase, ReqBase):
    pass

