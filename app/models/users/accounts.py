from sqlalchemy import Column, Integer, String, Date

from app.models.base import ModelBase


class UserAccount(ModelBase):
    _id = Column(Integer, autoincrement=True)  # 고유 ID
    
    id = Column(String, primary_key=True)  # 사용자 ID
    name = Column(String)  # 사용자 이름
    password = Column(String)  # 사용자 비밀번호
