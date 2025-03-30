from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.exc import InvalidRequestError, NoResultFound, SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.exceptions.base import BizException, SystemException
from app.core.logger import LOGGER
from app.schemas.systems.responses import ErrorResponse, JSendFailure

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.state.correlation_id

        try:
            response = await call_next(request)
            return response

        except BizException as exc:
            LOGGER.info(f"[Biz /{exc.status_code}] {exc.message}/{exc.detail=}/({correlation_id=})")

            return JSONResponse(
                status_code=exc.status_code,
                content=JSendFailure(
                    data=exc.message,
                ).model_dump()
            )

        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error", "details": str(exc)},
            )            
    # @staticmethod
    # async def handle(request: Request, exc: Exception):
    #     """모든 예외를 처리하는 글로벌 예외 처리기"""

    #     if isinstance(exc, BusinessException):
    #         LOGGER.info(f"[Error] [{exc.status_code}] {exc.detail}")            
    #         return await GlobalExceptionHandler._handle_biz_exception(request, exc)

    #     if isinstance(exc, SystemException):
    #         LOGGER.info(f"[Error] [{exc.status_code}] {exc.detail}")       
            

        
    #     # 예외 유형에 따라 처리
    #     if isinstance(exc, HTTPException):
    #         return await GlobalExceptionHandler._handle_http_exception(request, exc)
    #     elif isinstance(exc, SQLAlchemyError):
    #         return await GlobalExceptionHandler._handle_database_error(request, exc)
    #     else:
    #         return await GlobalExceptionHandler._handle_generic_error(request, exc)

    # @staticmethod
    # async def _handle_http_exception(request: Request, exc: HTTPException):
    #     LOGGER.error(f"[Error] [{exc.status_code}] {exc.detail}")
    #     return JSONResponse(
    #         status_code=exc.status_code,
    #         content=FailureResponse(
    #             code=exc.status_code,
    #             data={"message": str(exc.detail)},
    #         ).model_dump(),
    #     )

    # @staticmethod
    # async def _handle_biz_exception(request: Request, exc: BusinessException):
    #     LOGGER.info(f"[Error] [{exc.status_code}] {exc.detail}")

    #     return JSONResponse(
    #         status_code=exc.status_code,
    #         content=FailureResponse(
    #             status_code=exc.status_code,
    #             data={"message": str(exc.message)},
    #         ).model_dump(),
    #     )

    # @staticmethod
    # async def _handle_database_error(request: Request, exc: SQLAlchemyError):
    #     # SQLAlchemyError 처리
    #     if isinstance(exc, NoResultFound):
    #         return JSONResponse(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             content=FailureResponse(
    #                 code=status.HTTP_404_NOT_FOUND,
    #                 data={"message": str(exc)},
    #             ).model_dump(),
    #         )
    #     elif isinstance(exc, InvalidRequestError):
    #         return JSONResponse(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             content=FailureResponse(
    #                 code=status.HTTP_400_BAD_REQUEST,
    #                 data={"message": str(exc)},
    #             ).model_dump(),
    #         )
        
    #     # 일반 SQLAlchemyError 처리
    #     return JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content=ErrorResponse(
    #             code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             message=str(exc),
    #         ).model_dump(),
    #     )

    # @staticmethod
    # async def _handle_generic_error(request: Request, exc: Exception):
    #     """기타 예외를 처리"""
    #     LOGGER.error(f"[Error] [500] Unexpected error: {str(exc)}")
    #     return JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content=ErrorResponse(
    #             code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             message="Internal Server Error",
    #         ).model_dump(),
    #     )
