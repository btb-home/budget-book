from fastapi import status

from app.common.constants.systems import exc_msg
from app.common.exceptions.base import SystemException


class SysTestException(SystemException):
    def __init__(self, detail: str = exc_msg.SYS_TEST_EXCEPTION_MESSAGE):
        self.status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message: str = "System Test Exception"
        self.detail: str = detail
        
class RedisSystemException(SystemException):
    def __init__(self, detail: str = exc_msg.REDIS_SYSTEM_EXCEPTION_MESSAGE):
        self.status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message: str = "Redis System Exception"
        self.detail: str = detail


class RedisInitDataException(RedisSystemException):
    def __init__(self, detail: str = exc_msg.REDIS_INIT_DATA_EXCEPTION_MESSAGE):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = detail
