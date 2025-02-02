from sqlalchemy.orm import Session

from app.utils.decorators.db import transactional
from app.models.ledgers.expenses import LedgerExpense
from app.schemas.ledgers.expenses import LedgerExpenseBase, LedgerExpenseResponse
from app.schemas.ledgers.expenses import LedgerExpenseCreate
from app.crud.basic import select_all, select_one, insert

@transactional
async def fetch_expense_list(
    session: Session,
) -> list[LedgerExpense]:
    """
    Create a new ledger expense.
    """
    data = select_all(
        session, LedgerExpense, LedgerExpenseResponse
    )(orderby=LedgerExpense.transaction_date.name)
    
    return data


@transactional
async def create_expense(
    session: Session,
    ledger_expense_create: LedgerExpenseCreate,
) -> LedgerExpense:
    """
    Create a new ledger expense.
    """
    insert(session, LedgerExpense, LedgerExpenseCreate)(
        data=ledger_expense_create
    )
    return "done"


@transactional
async def fetch_expense_one(
    session: Session, id: int
) -> list[LedgerExpense]:
    """
    Create a new ledger expense.
    """
    data = select_one(
        session, LedgerExpense, LedgerExpenseResponse
    )(query={LedgerExpense.sid.name: id})

    return data