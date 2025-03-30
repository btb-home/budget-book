from enum import StrEnum, auto


class StatusCode(StrEnum):
    SUCCESS: str = auto()
    FAILURE: str = auto()
    ERROR: str = auto()
