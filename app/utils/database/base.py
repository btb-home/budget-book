from typing import Any, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.common.exceptions.biz import DataDuplicationException
from app.core.logger import LOGGER

T = TypeVar("T")  # Generic type for SQLAlchemy models


class DBClient:
    @staticmethod
    def insert(
        db: Session,
        schema: Type[T],
        model: BaseModel,
        unique_check_fields: list[str] | None = [],
    ) -> T | None:
        """
        Inserts a new record into the database.

        """
        db_session_id = db.db_session_id

        # 중복 검사 수행
        query_filter = {field: getattr(model, field) for field in unique_check_fields}
        existing = db.query(schema).filter_by(**query_filter).first()
        if existing:
            raise DataDuplicationException(f"{db_session_id} / {query_filter}")

        try:
            # 새 인스턴스 삽입
            instance = schema(**model.model_dump())
            db.add(instance)

            LOGGER.info(f"{db_session_id} / Inserting: {instance}")
            return instance
        except SQLAlchemyError as e:
            raise RuntimeError(f"{db_session_id} / Database Insert Error: {e}")

    @staticmethod
    def update(db: Session, model: Type[T], identifier: Any, data: BaseModel) -> T:
        """
        Updates an existing record in the database.

        """
        try:
            instance = db.query(model).get(identifier)
            if not instance:
                raise ValueError(f"Record with id {identifier} not found")

            for key, value in data.dict(exclude_unset=True).items():
                setattr(instance, key, value)

            db.commit()
            db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Database Update Error: {e}")
