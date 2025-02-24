from sqlalchemy import Column, Integer, String, Date

from app.models.base import BaseModel


class UserAccountRole(BaseModel):
    _id = Column(Integer, primary_key=True, autoincrement=True)  # 고유 ID
    
    account_id = Column(String)  # 사용자 ID
    role_id = Column(String)  # 역할 ID

    valid_yn = Column(String)  # 유효 여부
    start_date = Column(Date)  # 유효 시작일
    end_date = Column(Date)  # 유효 종료일