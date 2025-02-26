from pydantic import BaseModel
from app.schemas.base import ReqBase

class UserAccountBase(BaseModel):
    id: str
    name: str
    password: str
    
class UserAccountReq(UserAccountBase, ReqBase):
    pass
    