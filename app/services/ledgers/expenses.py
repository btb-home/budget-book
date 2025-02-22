from sqlalchemy.orm import Session

from app.utils.database.decorator import transactional
from app.models.ledgers.expenses import LedgerExpense
from app.schemas.ledgers.expenses import LedgerExpenseBase, LedgerExpenseResponse, LedgerExpenseCreate
from app.utils.database.basic import select_all, select_one, insert
from app.common.logging.logger import LOGGER

@transactional
async def fetch_expense_list(
    session: Session,
) -> list[LedgerExpense]:
    """
    Create a new ledger expense.
    """
    data = await select_all(
        session, LedgerExpense, LedgerExpenseResponse
    )(orderby=LedgerExpense.transaction_date.name)
    
    return data

@transactional
async def create_expense(
    db_session: Session,
    ledger_expense_create: LedgerExpenseCreate,
) -> LedgerExpense:
    """
    Create a new ledger expense.
    """
    res = insert(db_session, LedgerExpense, LedgerExpenseCreate)(
        data=ledger_expense_create
    )
    LOGGER.info(f"LedgerExpense Created: {res}")
    
    return {"data": str(res)}


@transactional
async def fetch_expense_one(
    session: Session, id: int
) -> list[LedgerExpense]:
    """
    Create a new ledger expense.
    """
    data = await select_one(
        session, LedgerExpense, LedgerExpenseResponse
    )(query={LedgerExpense.id.name: id})

    return data