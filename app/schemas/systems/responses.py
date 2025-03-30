from typing import Union

from pydantic import BaseModel, Field, model_validator

from app.common.constants.systems.codes import StatusCode
from app.schemas.systems import paginations as policy


class JSendResponse(BaseModel):
    status: StatusCode = StatusCode.SUCCESS
    code: int | None = Field(None, exclude=True)
    message: str | None = Field(None, exclude=True)
    data: dict | list | None = Field(None, exclude=True)

    class Config:
        from_attributes = True
        json_encoders = {
            BaseModel: lambda v: v.model_dump(),  # BaseModel을 자동으로 직렬화
        }


class JSendSuccess(JSendResponse):
    status: StatusCode = StatusCode.SUCCESS
    data: str | dict | list | BaseModel = Field(..., example="Success Response")
    pagination: Union[policy.PageBase, policy.OffsetBase, policy.CursorBase, None] = (
        Field(None, exclude=True)
    )

    @model_validator(mode="after")
    def populate_data_from_message(self):
        # data가 문자열일 때는 data를 {"message": data}로 변환
        if isinstance(self.data, str):
            self.data = {"message": self.data}

        # data가 비어 있고 message가 있을 경우 message를 data에 설정
        elif not self.data and self.message:
            self.data = {"message": self.message}

        return self


class JSendFailure(JSendResponse):
    status: StatusCode = StatusCode.FAILURE
    data: str | dict | list | BaseModel = Field(..., example="Success Response")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.FAILURE,
                "data": {"reason": "Failure Reason"},
            },
        }


class JSendError(JSendResponse):
    status: StatusCode = StatusCode.ERROR
    code: int = 500
    data: str | dict | list | BaseModel | None = Field(None, exclude=True)
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


class GetOneResponse(JSendSuccess):
    status: StatusCode = StatusCode.SUCCESS
    data: BaseModel | list[BaseModel] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.SUCCESS,
                "data": {"key1": "value1", "key2": "value2", "key3": "value3"},
            },
        }


class GetListResponse(JSendSuccess):
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
                    },
                ],
            },
        }


class GetListResponseWithPagination(JSendSuccess):
    status: StatusCode = StatusCode.SUCCESS
    data: list[BaseModel | dict] = []
    pagination: Union[policy.PageBase, policy.OffsetBase, policy.CursorBase] = Field(
        None, exclude=True
    )

    class Config:
        json_schema_extra = {
            "example": {
                # Request
                "status": StatusCode.SUCCESS,
                "data": [{"item1": "value1", "item2": "value2"}],
                "pagination": {
                    "page": 1,
                    "per_page": 10,
                    "total": 36,
                    "total_pages": 4,
                },
            },
        }
