# from sqlalchemy.orm import Session

# from app.core.logger import LOGGER
# from app.models.ledgers.expenses import LedgerExpense
# from app.schemas.ledgers.expenses import (
#     LedgerExpenseBase,
#     LedgerExpenseCreate,
#     LedgerExpenseRes,
# )
# from app.utils.database.basic import insert, select_all, select_one
# from app.utils.database.decorator import transactional


# @transactional
# async def fetch_expense_list(
#     db_session: Session,
# ) -> list[LedgerExpense]:
#     """
#     Create a new ledger expense.
#     """
#     data = select_all(db_session, LedgerExpense, LedgerExpenseRes)(
#         orderby=LedgerExpense.transaction_date.name
#     )

#     return data


# @transactional
# async def create_expense(
#     db_session: Session,
#     ledger_expense_create: LedgerExpenseCreate,
# ) -> LedgerExpense:
#     """
#     Create a new ledger expense.
#     """
#     res = insert(db_session, LedgerExpense, LedgerExpenseCreate)(
#         data=ledger_expense_create
#     )
#     LOGGER.info(f"LedgerExpense Created: {res}")

#     return res.as_dict()


# @transactional
# async def fetch_expense_one(db_session: Session, id: int) -> list[LedgerExpense]:
#     """
#     Create a new ledger expense.
#     """
#     data = select_one(db_session, LedgerExpense, LedgerExpenseRes)(
#         query={LedgerExpense.id.name: id}
#     )

#     return data
