from fastapi import APIRouter, Depends, Path, Body, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.utils.database.session import SessionMaker
from app.schemas.systems.responses import SuccessResponse, GetOneResponse, GetListResponse
from app.schemas.ledgers.expenses import LedgerExpenseCreate
import app.services.ledgers.expenses as svc

router = APIRouter()

@router.get("", response_model=GetListResponse)
async def get_ledger_expenses(session: Session = Depends(SessionMaker)) -> Response:
    
    data = await svc.fetch_expense_list(session)

    return SuccessResponse(
        data=data,
    )
    
@router.post("", response_model=SuccessResponse)
async def post_ledger_expenses(
    session: Session = Depends(SessionMaker),
    ledger_expense: LedgerExpenseCreate = Body(...),
) -> Response:
    
    data = await svc.create_expense(session, ledger_expense)

    return SuccessResponse(
        data=data,
    )

@router.get("/{id}", response_model=SuccessResponse)
async def get_ledger_expenses(
    session: Session = Depends(SessionMaker),
    id: int = Path(...),
) -> Response:
    
    data = await svc.fetch_expense_one(session, id)

    return GetOneResponse(
        data=data,
    )
    
@router.delete("/{id}", response_model=SuccessResponse)
async def delete_ledger_expenses(
    session: Session = Depends(SessionMaker),
    id: int = Path(...),
) -> Response:
    
    data = []

    return SuccessResponse(
        data=data,
    )
