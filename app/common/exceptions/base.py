from fastapi import status
from app.common.constants.systems import exceptions


class ProjectException(Exception):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "PROJECT Exception"
    detail = exceptions.PROJECT_EXCEPTION_DETAIL
    
class SystemException(ProjectException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "System Exception"
    detail = exceptions.SYSTEM_EXCEPTION_DETAIL

class DatabaseException(ProjectException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Database Exception"
    detail = exceptions.DATABASE_EXCEPTION_DETAIL

class BusinessException(ProjectException):
    code = status.HTTP_400_BAD_REQUEST
    message = "Business Exception"
    detail = exceptions.BUSINESS_EXCEPTION_DETAIL