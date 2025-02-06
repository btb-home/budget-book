from pydantic import BaseModel
from typing import Optional
from datetime import date

class LedgerExpenseBase(BaseModel):
    transaction_date: date  # 거래일 (지출일자)
    payment_method: str     # 결제 수단 (카드명)
    expense_type: str       # 지출 카테고리
    expense_detail_type: str = None # 지출 세부 카테고리
    expense_amount: int     # 지출 금액
    expense_unit: str       # 지출 단위
    expense_merchant_name: str  # 가맹점/거래처
    note: Optional[str] = None  # 비고 (지출 내용) - 선택적 필드

class LedgerExpenseCreate(LedgerExpenseBase):
    pass

class LedgerExpenseResponse(LedgerExpenseBase):
    id: int  # 고유 ID
    
    class Config:
        from_attributes = True  # SQLAlchemy 모델과 호환되도록 설정
 