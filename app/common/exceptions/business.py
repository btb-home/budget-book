from fastapi import status
from app.common.exceptions.base import BusinessException

class AuthenticationException(BusinessException):
    def __init__(self,  detail: str, url: str ="/"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail
        self.url = url 

class UserNotFoundException(BusinessException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail