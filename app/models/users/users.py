from sqlalchemy import Column, Integer, String, Date

from app.models.base import BaseModel


class BtbUser(BaseModel):
    _id = Column(Integer, primary_key=True, autoincrement=True)  # 고유 ID
    
    id = Column(String)  # 사용자 ID
    name = Column(String)  # 사용자 이름
    password = Column(String)  # 사용자 비밀번호

    permission_id = Column(String)  # 권한명
