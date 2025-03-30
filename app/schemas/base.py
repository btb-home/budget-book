import re
from datetime import datetime
from typing import Type

from pydantic import BaseModel as PySchema
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr

# Base class for SQLAlchemy models
moduleBase = declarative_base()


class ModelBase(moduleBase):
    __abstract__ = True

    # Audit columns
    creation_user_id = Column(String)
    creation_dttm = Column(DateTime, nullable=False, default=datetime.now)
    last_update_user_id = Column(String)
    last_update_dttm = Column(DateTime, onupdate=datetime.now)

    @declared_attr
    def __tablename__(cls):
        return _pascal_to_snake(cls.__name__)

    def create_date(self, user_id: str):
        """Set creation and update timestamps and user ID."""
        self.creation_user_id = user_id
        self.creation_dttm = datetime.now()
        self.last_update_user_id = user_id
        self.last_update_dttm = datetime.now()

    def update_date(self, user_id: str):
        """Update the timestamp and user ID for last update."""
        self.last_update_user_id = user_id
        self.last_update_dttm = datetime.now()

    def as_dict(self, excludes=None):
        """Return the model as a dictionary, excluding specified columns."""
        excludes = excludes or []
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in excludes
        }

    def to_pydantic(self, schema_cls: Type[PySchema]) -> PySchema:
        """
        Convert the SQLAlchemy model instance to a Pydantic model instance.
        """
        data = {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
        return schema_cls(**data)

    def __str__(self):
        """String representation of the model instance."""
        attrs = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ]
        attr_str = ", ".join([f"{attr}={getattr(self, attr)}" for attr in attrs])
        return f"{self.__class__.__name__}({attr_str})"

    def __repr__(self):
        """Representation of the model instance."""
        return f"<{self.__class__.__name__}>"


def _pascal_to_snake(input_string: str):
    """Convert PascalCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", input_string).lower()
