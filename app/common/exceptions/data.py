from fastapi import status
from sqlalchemy.exc import NoResultFound

from app.common.constants.systems import exc_msg
from app.common.exceptions.base import DataException


class NoResultFound(NoResultFound):
    pass


class DuplicateDataException(DataException):
    def __init__(self, db_session_id: str, detail: str = ""):
        self.status_code = status.HTTP_409_CONFLICT
        self.message = exc_msg.DUPLICATE_DATA_EXCEPTION_MESSAGE
        self.detail = f"({db_session_id}) {self.message} {detail}"
