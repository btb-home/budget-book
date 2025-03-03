from fastapi import status
from app.common.exceptions.base import BusinessException
from app.common.constants.systems import exceptions

class AuthenticationException(BusinessException):
    def __init__(self,  detail: str, url: str ="/"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail
        self.url = url 

class UserAuthenticationFail(BusinessException):
    def __init__(self, detail: str = ""):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = exceptions.USER_AUTHENTICATION_FAIL_DETAIL
        self.detail= f"{self.message} - {detail}"