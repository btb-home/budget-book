from fastapi import Header

from app.schemas.systems.headers import YabasCommonHeader


def set_v1_bknd_common_header(
    headers: YabasCommonHeader = Header(None),
):
    return headers
