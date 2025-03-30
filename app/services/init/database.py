# app/utils/database/initializer.py

import json
from pathlib import Path

from sqlalchemy.orm.session import Session

from app.common.exceptions.biz import DataDuplicationException
from app.core.configs import AppConfig
from app.core.databases import engine
from app.core.logger import LOGGER
from app.models.users.accounts import UserAccountReq
from app.schemas.base import ModelBase
from app.schemas.users.accounts import UserAccount
from app.utils.common.files import read_file
from app.utils.database.base import DBClient

# from app.utils.database.basic import insert
from app.utils.database.decorator import transactional


async def init_database_data():
    """
    데이터베이스 초기화 작업을 수행하는 함수입니다.

    이 함수는 데이터베이스 테이블을 생성하고, 초기 데이터를 로드하여
    `UserAccount` 테이블에 데이터를 삽입하거나 업데이트하는 작업을 수행합니다.

    초기화 작업은 트랜잭션 내에서 진행되며, 오류 발생 시 롤백됩니다.
    """
    try:
        # 데이터베이스 테이블 생성
        ModelBase.metadata.create_all(bind=engine)
        LOGGER.info("[   DB] 데이터베이스 테이블 생성 초기화 완료")

        # 데이터베이스 초기 데이터 로드 및 삽입
        await init_db_data("common", "user_account")
        LOGGER.info("[   DB] 데이터베이스 데이터 초기 세팅 완료")

    except Exception as e:
        LOGGER.error(f"[   DB] 초기화 작업 중 오류 발생: {e}")
        raise e


@transactional
async def init_db_data(data_schema: str, name: str, db_session: Session):
    """
    데이터베이스 초기 데이터를 삽입합니다.

    이 함수는 각 테이블에 맞는 데이터를 삽입하는 작업을 진행합니다.
    """
    try:
        user_accounts_data = load_initial_data(data_schema, name)
        user_account = [
            UserAccountReq.model_validate(user) for user in user_accounts_data
        ]

        for data in user_account:
            # 비밀번호 필드 처리
            data.password = data.password.get_secret_value()
            try:
                DBClient.insert(
                    db_session,
                    UserAccount,
                    data,
                    unique_check_fields=[UserAccount.id.name],
                )
            except DataDuplicationException as e:
                table_name = UserAccount.__tablename__
                LOGGER.warning(
                    f"[   DB] {e.detail} - 테이블: {table_name} 데이터: {data.id}"
                )

    except Exception as e:
        LOGGER.error(f"[   DB] 데이터 초기화 실패: {e}")
        raise e


def load_initial_data(data_schema: str, name: str) -> list:
    """
    초기 데이터를 로드하는 함수입니다.

    :param data_schema: 데이터 스키마 폴더
    :param name: 데이터 파일 이름
    :return: 로드된 데이터 리스트 또는 빈 리스트
    """
    resources_path = _get_resource_path(data_schema, name)

    try:
        read_data = read_file(resources_path)
        return json.loads(read_data)
    except Exception as e:
        LOGGER.error(
            f"[   DB] 초기 데이터 로드 실패: {e} - 파일 경로: {resources_path}"
        )
        return []


def _get_resource_path(data_schema: str, name: str) -> Path:
    """
    지정된 데이터 파일의 경로를 반환합니다.

    :param data_schema: 데이터 스키마 폴더
    :param name: 데이터 파일 이름
    :return: 파일 경로
    """
    root_path = Path(AppConfig.ROOT_DIR)
    return root_path / "data" / "resources" / "init-data" / data_schema / f"{name}.json"
