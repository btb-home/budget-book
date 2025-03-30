from typing import Any, Dict

from pydantic import BaseModel


class ReqBase(BaseModel):
    pass


class ResBase(BaseModel):
    class Config:
        from_attributes = True
