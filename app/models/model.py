import re
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr

moduleBase = declarative_base()


class BaseModel:
    @declared_attr  # type: ignore
    def __tablename__(cls):
        s1 = str(cls.__name__)  # type:ignore
        output = _pascal_to_snake(s1)
        return output

    def __str__(self):
        # 클래스의 속성들을 가져옴
        attrs = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ]
        # 가져온 속성들을 문자열로 변환
        attr_str = ", ".join([f"{attr}={getattr(self, attr)}" for attr in attrs])
        return f"{self.__class__.__name__}({attr_str})"

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


class YabasBaseModel(BaseModel):
    __abstract__ = True
    __table_args__ = {'extend_existing': True} 

    # Audit Column
    created_dttm = Column(DateTime, nullable=False, default=datetime.now)
    created_owner_uid = Column(String)
    modified_dttm = Column(DateTime, onupdate=datetime.now)
    modified_owner_uid = Column(String)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def _pascal_to_snake(input_string: str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", input_string).lower()

class YabasModel(moduleBase, YabasBaseModel):
    __abstract__ = True

    class Config:
        from_attributes = True