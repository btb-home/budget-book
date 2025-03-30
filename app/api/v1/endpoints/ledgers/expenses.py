from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

import app.services.endpoints.ledgers.expenses as svc
from app.schemas.ledgers.expenses import LedgerExpenseCreate
from app.schemas.systems.responses import (
    GetListResponse,
    GetOneResponse,
    JSendSuccess,
)
from app.utils.database.db_session import get_sync_session

router = APIRouter()


@router.get("", response_model=GetListResponse)
async def get_ledger_expenses() -> Response:

    data = await svc.fetch_expense_list()

    return JSendSuccess(
        data=data,
    )


@router.post("", response_model=JSendSuccess)
async def post_ledger_expenses(
    ledger_expense: LedgerExpenseCreate = Body(...),
) -> Response:

    data = await svc.create_expense(ledger_expense)

    return JSendSuccess(
        data=data,
    )


@router.get("/{id}", response_model=JSendSuccess)
async def get_ledger_expenses(
    id: int = Path(...),
) -> Response:

    data = await svc.fetch_expense_one(id)

    return GetOneResponse(
        data=data,
    )


@router.delete("/{id}", response_model=JSendSuccess)
async def delete_ledger_expenses(
    id: int = Path(...),
) -> Response:

    data = []

    return JSendSuccess(
        data=data,
    )
