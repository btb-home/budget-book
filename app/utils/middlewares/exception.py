from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import InvalidRequestError, NoResultFound, SQLAlchemyError

from app.core.logger import LOGGER
from app.schemas.systems.responses import FailureResponse, ErrorResponse

class ClientErrorHandler:
    @staticmethod
    async def handle(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=FailureResponse(
                code=exc.status_code,
                data={"message": str(exc.detail)},
            ).model_dump(),  # .dict()를 사용해 객체를 딕셔너리로 변환
        )


class ServerErrorHandler:
    @staticmethod
    async def handle(request: Request, exc: Exception):
        LOGGER.error(exc, exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
            ).model_dump(),  # .dict()를 사용해 객체를 딕셔너리로 변환
        )


class DatabaseErrorHandler:
    @staticmethod
    async def handle(request: Request, exc: SQLAlchemyError):

        if isinstance(exc, NoResultFound):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=FailureResponse(
                    code=status.HTTP_404_NOT_FOUND,
                    data={"message": str(exc)},
                ).model_dump(),  # .dict()를 사용해 객체를 딕셔너리로 변환
            )
        elif isinstance(exc, InvalidRequestError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=FailureResponse(
                    code=status.HTTP_400_BAD_REQUEST,
                    data={"message": str(exc)},
                ).model_dump(),  # .dict()를 사용해 객체를 딕셔너리로 변환
            )

        # else: SQLAlchemyError
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(exc),
            ).model_dump(),  # .dict()를 사용해 객체를 딕셔너리로 변환
        )
