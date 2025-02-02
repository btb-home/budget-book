from fastapi import APIRouter, Depends, Path, Body, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.systems.responses import SuccessResponse, GetOneResponse, GetListResponse
from app.schemas.ledgers.expenses import LedgerExpenseCreate
import app.services.ledgers.expenses as svc

router = APIRouter()

@router.get("", response_model=GetListResponse)
async def get_ledger_expenses(session: Session = Depends(get_session)) -> Response:
    
    data = []

    return SuccessResponse(
        data=data,
    )
    
@router.post("", response_model=SuccessResponse)
async def post_ledger_expenses(
    session: Session = Depends(get_session),
    ledger_expense: LedgerExpenseCreate = Body(...),
) -> Response:
    
    data = await svc.create_expense(session, ledger_expense)

    return SuccessResponse(
        data=data,
    )

@router.delete("/{id}", response_model=SuccessResponse)
async def delete_ledger_expenses(
    session: Session = Depends(get_session),
    id: str = Path(...),
) -> Response:
    
    data = []

    return SuccessResponse(
        data=data,
    )
