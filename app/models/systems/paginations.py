from pydantic import BaseModel

DEFAULT_PAGE_SIZE = 10


class Pagination(BaseModel):
    pass


class PageBase(Pagination):
    page: int = 1
    page_size: int = DEFAULT_PAGE_SIZE
    total_items: int = 0
    total_pages: int = 1


class OffsetBase(Pagination):
    offset: int = 0
    limit: int = DEFAULT_PAGE_SIZE
    total_items: int = 0


class CursorBase(Pagination):
    cursor: str = ""
    limit: int = DEFAULT_PAGE_SIZE
