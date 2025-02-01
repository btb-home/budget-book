from fastapi import status
from fastapi.exceptions import HTTPException

from functools import wraps

from sqlalchemy.exc import InvalidRequestError, NoResultFound, SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

# from app.core.logger import logger


# 트랜잭션 데코레이터
def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        if not session:
            session = _get_session(args)

        try:
            result = await func(*args, **kwargs)
            print(result)

            session.commit()
            print("Transaction Committed")
            return result

        except IntegrityError as e:
            print(e._message())
            session.rollback()
            raise HTTPException(status.HTTP_409_CONFLICT, type(e).__name__)

        except NoResultFound as e:
            print(e._message())
            session.rollback()
            raise HTTPException(status.HTTP_404_NOT_FOUND, e._message())
            
        except InvalidRequestError as e:
            print(e._message())
            session.rollback()
            raise HTTPException(status.HTTP_400_BAD_REQUEST, e._message())

        except SQLAlchemyError as e:
            print(e._message())
            session.rollback()
            raise SQLAlchemyError(f"Internal DB Error")

        finally:
            session.close()

    return wrapper


# 커넥션 관리 데코레이터
def connectional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        if not session:
            session = _get_session(args)

        try:
            result = await func(*args, **kwargs)
            return result

        except NoResultFound as e:
            print(e._message())
            raise HTTPException(status.HTTP_404_NOT_FOUND, e._message())
            
        except InvalidRequestError as e:
            print(e._message())
            raise HTTPException(status.HTTP_400_BAD_REQUEST, e._message())

        except SQLAlchemyError as e:
            print(e._message())
            raise SQLAlchemyError(f"Internal DB Error")

        finally:
            session.close()

    return wrapper


# 공통 로직: 세션을 가져오고 처리하는 함수
def _get_session(args):
    session = next((arg for arg in args if isinstance(arg, Session)), None)
    if session is None:
        raise ValueError("No Session object found in arguments")

    return session
