from sqlalchemy import Column, Integer, String, Date

from app.models.base import BaseModel


class UserRolePolicy(BaseModel):
    _id = Column(Integer, primary_key=True, autoincrement=True)  # 고유 ID
    
    id = Column(String)  # 정책 ID
    name = Column(String)  # 정책 명

    key = Column(String)  # 정책 키
    value = Column(String)  # 정책 값
    