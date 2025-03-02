from sqlalchemy.orm import Session

import app.models.users.accounts as db_model
import app.schemas.users.accounts as py_schema
from app.utils.database.decorator import transactional
from app.utils.database.basic import select_one, insert
from app.core.logger import LOGGER

@transactional
async def sign_in(
    user_signin_req: py_schema.UserSingIn,
    db_session: Session,
) -> list[py_schema.UserAccountRes]:
    """
    Create a new ledger account.
    """
    data = select_one(
        db_session, db_model.UserAccount, py_schema.UserSingIn
    )(query={
        db_model.UserAccount.id.name: user_signin_req.id,
        db_model.UserAccount.password.name: user_signin_req.password,
    })

    if not data:
        raise Exception("User Account Not Found")
    
    res_data = data # .to_res()
    LOGGER.info(f"User Account Fetched: {res_data}")
        
    return res_data

@transactional
async def sign_out(
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
