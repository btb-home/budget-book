from pydantic import BaseModel
from typing import Any, Dict


class ReqBase(BaseModel):
    pass


class ResBase(BaseModel):
    class Config:
        from_attributes = True