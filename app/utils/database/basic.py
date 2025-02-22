from typing import List

from pydantic import BaseModel as PySchema
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

# from app.core.logger import logger
from app.models.base import BaseModel
from app.common.logging.logger import LOGGER

def insert(db_session: Session, model_cls: BaseModel, schema_cls: PySchema) -> BaseModel:
    """
    ## 데이터 단건 생성
    """

    def _inner(data: PySchema, upsert: bool = False):
        # Input
        obj = model_cls(**data.model_dump())

        # Process
        if upsert:
            obj = db_session.merge(obj)
        else:
            db_session.add(obj)

        db_session.flush()
        db_session.refresh(obj)

        LOGGER.info(f"'{model_cls.__tablename__}' Inserted: {data}, Upsert : {upsert}")

        # Output
        return obj

    return _inner


def update(db: Session, model_cls: BaseModel, schema_cls: PySchema) -> PySchema:
    """
    ## 데이터 단건 수정
    """

    def _inner(key: dict, data: PySchema) -> PySchema:
        # Insert
        query_filters = [col == val for col, val in key.items()]

        # 쿼리 작성
        stmt = (
            db.query(model_cls)
            .filter(*query_filters)
        )

        LOGGER.info(
            f"Query: {model_cls.__tablename__}, Filters: {len(query_filters)}, "
        )

        # 쿼리 수행
        res = stmt.first()

        if res is None:
            raise NoResultFound(f"Data not found")
        
        update_data = data.model_dump(exclude_unset=True)
        [setattr(res, key, value) for key, value in update_data.items()]
        
        # Output
        return data.model_validate(res)

    return _inner


def select_all(
    db: Session, model_cls: BaseModel, schema_cls: PySchema
) -> List[BaseModel]:
    """
    ## 데이터 다건 조회 기본
    """

    def _inner(
        query: dict = None, orderby: str = None, asc: bool = True, limit: int = 10, offset: int = 0,
    ):
        # 쿼리 조건 설정
        query = query or dict()
        query_filters = [getattr(model_cls, col) == val for col, val in query.items()]

        # 정렬 처리
        orderby = orderby or model_cls.created_dttm.name
        orderby_column = getattr(model_cls, orderby)
        orderby_expression = orderby_column.asc() if asc else orderby_column.desc()

        # 쿼리 작성
        stmt = (
            db.query(model_cls)
            .filter(*query_filters)
            .order_by(orderby_expression)
            .limit(limit)
            .offset(offset)
        )

        LOGGER.info(
            f"Query: {model_cls.__tablename__}, Filters: {query}, "
            f"Order by: {orderby} ({'ASC' if asc else 'DESC'}), Limit: {limit} (Offset: {offset})"
        )

        # 쿼리 수행
        res = stmt.all()

        return [schema_cls.model_validate(r) for r in res]

    return _inner


def select_one(
    db: Session, model_cls: BaseModel, schema_cls: PySchema
) -> BaseModel | None:
    """
    ## 데이터 단건 조회 기본
    """

    def _inner(query: dict = None, required: bool = False):
        # 쿼리 조건 설정
        query = query or dict()

        result = select_all(db, model_cls, schema_cls)(
            query=query, orderby="created_dttm", asc=True, limit=1, offset=0
        )

        # 결과 처리
        if result is None or len(result) == 0:
            if required:
                raise NoResultFound("Data not found")
            return None

        return result[0].model_dump()

    return _inner


def exists(
    db: Session, model_cls: BaseModel, schema_cls: PySchema
) -> bool:
    """
    ## 데이터 단건 존재 여부 파악
    """

    def _inner(query: dict):
        # 쿼리 조건 설정
        query_filters = [col == val for col, val in query.items()]

        # 존재 여부 쿼리 작성
        stmt = db.query(model_cls).filter(*query_filters)

        LOGGER.info(
            f"Exists Query: {model_cls.__tablename__}, Filters: {query}"
        )

        # 존재 여부 확인
        return db.query(stmt.exists()).scalar()

    return _inner


def delete(db: Session, model_cls: BaseModel, schema_cls: PySchema) -> None:
    """
    ## 데이터 단건 삭제
    """

    def _inner(key: dict) -> None:
        query_filters = [col == val for col, val in key.items()]
        res = db.query(model_cls).filter(*query_filters).all()

        # 쿼리 작성
        stmt = (
            db.query(model_cls)
            .filter(*query_filters)
        )

        LOGGER.info(
            f"Query: {model_cls.__tablename__}, Filters: {len(query_filters)}, "
        )

        # 쿼리 수행
        res = stmt.first()
        
        if res is None:
            raise NoResultFound(f"Data not found")

        stmt.delete()
        return None

    return _inner
