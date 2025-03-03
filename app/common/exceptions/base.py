from fastapi import status
from app.common.constants.systems import exc_msg


class ProjectException(Exception):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "PROJECT Exception"
    detail = exc_msg.PROJECT_EXCEPTION_MESSAGE


class BusinessException(ProjectException):
    code = status.HTTP_400_BAD_REQUEST
    message = "Business Exception"
    detail = exc_msg.BUSINESS_EXCEPTION_MESSAGE


class SystemException(ProjectException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "System Exception"
    detail = exc_msg.SYSTEM_EXCEPTION_MESSAGE


class DataException(ProjectException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Data Exception"
    detail = exc_msg.DATA_EXCEPTION_MESSAGE
