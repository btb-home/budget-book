from sqlalchemy.orm import Session

import app.models.users.accounts as db_model
import app.schemas.users.accounts as py_schema
from app.utils.database.decorator import transactional, connectional
from app.utils.database.basic import select_all, select_one, insert
from app.core.logger import LOGGER

@transactional
async def fetch_account_list(
    db_session: Session,
) -> list[py_schema.UserAccountRes]:
    """
    Create a new ledger account.
    """
    data = select_all(
        db_session, db_model.UserAccount, py_schema.UserAccountBase
    )(orderby=db_model.UserAccount.id.name)
    
    res_data = [d.to_res() for d in data]
    LOGGER.info(f"User Account Fetched: {res_data}")
        
    return res_data

@transactional
async def create_account(
    user_account_req: py_schema.UserAccountReq,
    db_session: Session,
) -> py_schema.UserAccountRes:
    """
    Create a new ledger account.
    """
    res = insert(
        db_session, db_model.UserAccount, py_schema.UserAccountBase
    )(data=user_account_req, upsert=True)

    res_data = res.to_res()
    LOGGER.info(
        f"User Account Created: {type(res_data)}, {res_data}, {type(res_data.model_dump())},{res_data.model_dump()}"
    )
    
    return res_data


@connectional
async def fetch_account_one(
    id: str,
    db_session: Session,
) -> py_schema.UserAccountRes:
    """
    Create a new ledger account.
    """
    data = select_one(
        db_session, db_model.UserAccount, py_schema.UserAccountBase
    )(query={db_model.UserAccount.id.name: id})
    
    res_data = data.to_res()
    LOGGER.info(f"User Account Fetched: {res_data}")

    return res_data