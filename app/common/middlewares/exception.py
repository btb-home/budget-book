import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.constants.systems.exc_msg import SYSTEM_EXCEPTION_MESSAGE
from app.common.exceptions.base import BizException, SysException
from app.core.logger import LOGGER
from app.models.systems.responses import JSendError, JSendFailure


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = getattr(request.state, "correlation_id", "unknown")

        try:
            return await call_next(request)

        except BizException as exc:
            except_message = exc.message
            detail_message = exc.detail

            LOGGER.info(
                f"[Biz   /500] ({correlation_id=}) {except_message}: {detail_message} "
            )
            return JSONResponse(
                status_code=exc.status_code,
                content=JSendFailure(
                    data=except_message, message=detail_message
                ).model_dump(),
            )

        except SysException as exc:
            except_message = exc.message
            detail_message = exc.detail

            LOGGER.warning(
                f"[Sys   /500] ({correlation_id=}) {except_message}: {detail_message} "
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=JSendError(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=SYSTEM_EXCEPTION_MESSAGE,
                ).model_dump(),
            )

        except Exception as exc:
            except_message = type(exc).__name__
            detail_message = f"{str(exc)}\n{traceback.format_exc()}"

            LOGGER.error(
                f"[Unknown/500] ({correlation_id=}) {except_message}: {detail_message} "
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=JSendError(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=SYSTEM_EXCEPTION_MESSAGE,
                ).model_dump(),
            )
