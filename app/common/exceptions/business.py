from fastapi import status

from app.common.constants.systems import exc_msg
from app.common.exceptions.base import BusinessException


class AuthenticationException(BusinessException):
    def __init__(self, detail: str, url: str = "/"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail
        self.url = url


class UserAuthenticationFail(BusinessException):
    def __init__(self, detail: str = ""):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = exc_msg.USER_AUTHENTICATION_FAIL_MESSAGE
        self.detail = f"{self.message} - {detail}"


# Session Exceptions
class SessionException(BusinessException):
    def __init__(self, detail: str = ""):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail


class SessionNotFoundException(SessionException):
    def __init__(self, detail: str = ""):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = exc_msg.SESSION_NOT_FOUND_EXCEPTION_MESSAGE
        self.detail = f"{self.message} - {detail}"


class SessionGuestBannedException(SessionException):
    def __init__(self, detail: str = ""):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.message = exc_msg.SESSION_GUEST_BANNED_EXCEPTION_MESSAGE
        self.detail = f"{self.message} - {detail}"


class SessionExpiredException(SessionException):
    def __init__(self, detail: str = ""):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = exc_msg.SESSION_EXPIRED_EXCEPTION_MESSAGE
        self.detail = f"{self.message} - {detail}"
