from typing import List

from pydantic import BaseModel as PySchema
from sqlalchemy.orm import Session

from app.core.logger import LOGGER
from app.models.base import ModelBase
from app.common.exceptions.database import NoResultFound

def insert(db: Session, model_cls: ModelBase, schema_cls: PySchema) -> PySchema:
    """
    ## 데이터 단건 생성
    """
    def _inner(data: PySchema, upsert: bool = False) -> PySchema:
        obj = model_cls(**data.model_dump())

        if upsert:
            stmt = db.merge(obj)
        else:
            db.add(obj)
            stmt = obj

        db.flush()
        db.refresh(stmt)

        LOGGER.info (f"[   DB] Insert: ({model_cls.__tablename__})")
        LOGGER.debug(f"[   DB] Insert: ({model_cls.__tablename__}), Data={data}, Upsert={upsert}")

        res_dict = stmt
        return schema_cls.model_validate(res_dict.__dict__)

    return _inner

def update(db: Session, model_cls: ModelBase, schema_cls: PySchema) -> PySchema:
    """
    ## 데이터 단건 수정
    """
    def _inner(key: dict, data: PySchema) -> PySchema:
        query_filters = [getattr(model_cls, col) == val for col, val in key.items()]

        stmt = db.query(model_cls).filter(*query_filters)

        LOGGER.info (f"[   DB] Update: ({model_cls.__tablename__})")
        LOGGER.debug(f"[   DB] Update: ({model_cls.__tablename__}), Data={data}, Filters={key}")

        res = stmt.first()

        if not res:
            raise NoResultFound("Data not found")

        update_data = data.model_dump(exclude_unset=True)
        for col, val in update_data.items():
            setattr(res, col, val)

        db.flush()
        db.refresh(res)

        res_dict = stmt 
        return schema_cls.model_validate(res_dict.__dict__)

    return _inner

def select_all(db: Session, model_cls: ModelBase, schema_cls: PySchema) -> List[PySchema]:
    """
    ## 데이터 다건 조회 기본
    """
    def _inner(query: dict = None, orderby: str = None, asc: bool = True, limit: int = 10, offset: int = 0) -> List[PySchema]:
        query = query or {}
        query_filters = [getattr(model_cls, col) == val for col, val in query.items()]

        orderby = orderby or model_cls.creation_dttm.name
        orderby_column = getattr(model_cls, orderby)
        orderby_expression = orderby_column.asc() if asc else orderby_column.desc()

        stmt = (
            db.query(model_cls)
            .filter(*query_filters)
            .order_by(orderby_expression)
            .limit(limit)
            .offset(offset)
        )

        LOGGER.info (f"[   DB] Select: ({model_cls.__tablename__})")
        LOGGER.debug(f"[   DB] Select: ({model_cls.__tablename__}), OrderBy={orderby}, ASC={asc}, Limit={limit}, Offset={offset}")

        res = stmt.all()
        return [schema_cls.model_validate(r.__dict__) for r in res]

    return _inner

def select_one(db: Session, model_cls: ModelBase, schema_cls: PySchema) -> PySchema | None:
    """
    ## 데이터 단건 조회 기본
    """
    def _inner(query: dict = None) -> PySchema | None:
        query = query or {}

        result = select_all(db, model_cls, schema_cls)(
            query=query, orderby="creation_dttm", asc=True, limit=1, offset=0
        )

        if result:
            return result[0]

        return None

    return _inner

def exists(db: Session, model_cls: ModelBase) -> bool:
    """
    ## 데이터 단건 존재 여부 파악
    """
    def _inner(query: dict) -> bool:
        query_filters = [getattr(model_cls, col) == val for col, val in query.items()]
        stmt = db.query(model_cls).filter(*query_filters)

        LOGGER.info (f"[   DB] Exists: ({model_cls.__tablename__})")
        LOGGER.debug(f"[   DB] Exists: ({model_cls.__tablename__}), query={query}")

        return db.query(stmt.exists()).scalar()

    return _inner

def delete(db: Session, model_cls: ModelBase) -> None:
    """
    ## 데이터 단건 삭제
    """
    def _inner(key: dict) -> None:
        query_filters = [getattr(model_cls, col) == val for col, val in key.items()]

        stmt = db.query(model_cls).filter(*query_filters)

        LOGGER.info (f"[   DB] Delete: ({model_cls.__tablename__})")
        LOGGER.debug(f"[   DB] Delete: ({model_cls.__tablename__}), Filters={key}")

        res = stmt.first()

        if res is None:
            raise NoResultFound("Data not found")

        db.delete(res)
        db.flush()

    return _inner