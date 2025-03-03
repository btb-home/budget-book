from sqlalchemy import Column, String, DateTime, Boolean

from app.models.base import ModelBase


class UserAccount(ModelBase):
    id = Column(String, primary_key=True, comment="ID")
    name = Column(String, comment="이름")
    password = Column(String, comment="비밀번호")

    admin_role_yn = Column(Boolean, default=False, comment="관리자 역할 여부")
    last_login_dttm = Column(DateTime, nullable=True, comment="마지막 로그인 일시")
    last_login_ip = Column(String, nullable=True, comment="마지막 로그인 IP")

# PySchema
import app.schemas.users.accounts