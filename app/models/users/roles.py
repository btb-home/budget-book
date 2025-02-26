from sqlalchemy import Column, Integer, String, Date

from app.models.base import ModelBase


class UserRole(ModelBase):
    _id = Column(Integer, primary_key=True, autoincrement=True)  # 고유 ID
    
    id = Column(String)  # 역할 ID
    name = Column(String)  # 역할명
    description = Column(String)  # 역할 설명
    