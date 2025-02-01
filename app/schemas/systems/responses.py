from typing import Union
from pydantic import BaseModel, Field, model_validator

from app.schemas.systems import paginations as policy
from app.constants.systems.status_code import StatusCode

class JSendResponse(BaseModel):
    status: StatusCode
    code: int | None = Field(None, exclude=True)
    message: str | None = Field(None, exclude=True)
    data: dict | list | None = Field(None, exclude=True)
        
class SuccessResponse(JSendResponse):
    status: StatusCode = StatusCode.SUCCESS
    data: dict | list = {}
    pagination: Union[
        policy.PageBase,
        policy.OffsetBase,
        policy.CursorBase,
        None
    ] = Field(None, exclude=True)

    @model_validator(mode="after")
    def populate_data_from_message(self):
        # self.data가 비어 있고 self.message가 있으면 data에 message 값 설정
        if not self.data and self.message:
            self.data = {"message": self.message}
        return self
    
class FailureResponse(JSendResponse):
    status: StatusCode = StatusCode.FAILURE
    data: dict = {}

    class Config:
        json_schema_extra = {
            "example": {
                    # Request
                    "status": StatusCode.FAILURE,
                    "data": {"reason": "Failure Reason"},
                },
        }    
            
class ErrorResponse(JSendResponse):
    status: StatusCode = StatusCode.ERROR
    code: int = 500
    message: str = "Internal Server Error"

    class Config:
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.ERROR,
                "code": 500,
                "message": "Internal Server Error",
            },
        }
    
class GetOneResponse(SuccessResponse):
    status: StatusCode = StatusCode.SUCCESS
    data: dict = {}

    class Config:
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.SUCCESS,
                "data": {
                    "key1": "value1",
                    "key2": "value2",
                    "key3": "value3"
                },
            },
        }
        
class GetListResponse(SuccessResponse):
    status: StatusCode = StatusCode.SUCCESS
    data: list  = []

    class Config:
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.SUCCESS,
                "data": [
                    {
                        "key1": "value1",
                        "key2": "value2",
                    },
                    {
                        "key1": "value1",
                        "key2": "value2",
                    }
                ],
            },
        }

class GetListResponseWithPagination(SuccessResponse):
    status: StatusCode = StatusCode.SUCCESS
    data: list[dict] = []
    pagination: Union[
        policy.PageBase,
        policy.OffsetBase,
        policy.CursorBase
    ] = Field(None, exclude=True)

    class Config:
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.SUCCESS,
                "data": [
                    {
                        "item1": "value1", 
                        "item2": "value2"
                    }
                ],
                "pagination": {
                    "page": 1,
                    "per_page": 10,
                    "total": 36,
                    "total_pages": 4
                },
            },
        }

class ActionResponse(SuccessResponse):
    status: StatusCode = StatusCode.SUCCESS
    message: str = "Request Submitted"
    data: dict | None = None

    class Config:
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.SUCCESS,
                "message": "Request Submitted",
            },
        }