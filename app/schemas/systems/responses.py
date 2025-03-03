from typing import Union
from pydantic import BaseModel, Field, model_validator

from app.schemas.systems import paginations as policy
from app.common.constants.systems.codes import StatusCode

class JSendResponse(BaseModel):
    status: StatusCode
    code: int | None = Field(None, exclude=True)
    message: str | None = Field(None, exclude=True)
    data: dict | list | None = Field(None, exclude=True)
    
    class Config:
        from_attributes = True

class SuccessResponse(JSendResponse):
    status: StatusCode = StatusCode.SUCCESS
    data: str | dict | list | BaseModel = Field(..., example="Success Response")
    pagination: Union[
        policy.PageBase,
        policy.OffsetBase,
        policy.CursorBase,
        None
    ] = Field(None, exclude=True)

    @model_validator(mode="after")
    def populate_data_from_message(self):
        # data가 문자열일 때는 data를 {"message": data}로 변환
        if isinstance(self.data, str):
            self.data = {"message": self.data}
        
        # data가 비어 있고 message가 있을 경우 message를 data에 설정
        elif not self.data and self.message:
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
    data: BaseModel | list[BaseModel] = Field(...)

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
    data: list = Field(...)

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
    data: list[BaseModel | dict] = []
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
    data: str | dict | list | BaseModel = Field(None, example="Success Response")
    message: str = "Request Submitted"

    class Config:
        json_schema_extra = {
            "example": {
                "status": StatusCode.SUCCESS,
                "message": "Request Submitted",
            },
        }