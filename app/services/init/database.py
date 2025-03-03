from app.models.base import ModelBase
from app.core.databases import engine
from app.core.logger import LOGGER
from app.services.init.data import load_init_data
from app.schemas.users.accounts import UserAccountReq
from app.models.users.accounts import UserAccount
from app.utils.database.basic import insert
from app.utils.database.decorator import transactional
from sqlalchemy.orm.session import Session

@transactional
async def init_database(db_session: Session):
    # 데이터베이스 스키마 생성
    ModelBase.metadata.create_all(bind=engine)
    LOGGER.info("Database initialized")

    # 데이터 로드 및 초기화
    user_accounts = await load_init_data("common", "user_account")
    user_account = [UserAccountReq.model_validate(user) for user in user_accounts]

    for data in user_account:
        insert(db_session, UserAccount, UserAccountReq)(data, upsert=True)
