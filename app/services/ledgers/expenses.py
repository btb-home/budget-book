from sqlalchemy.orm import Session

from app.utils.decorators.db import transactional
from app.models.ledgers.expenses import LedgerExpense
from app.schemas.ledgers.expenses import LedgerExpenseCreate
from app.crud.basic import insert

@transactional
async def create_expense(
    session: Session,
    ledger_expense: LedgerExpenseCreate,
) -> LedgerExpense:
    """
    Create a new ledger expense.
    """
    insert(session, LedgerExpense, LedgerExpenseCreate)(
        ledger_expense
    )
    
    return "done"
