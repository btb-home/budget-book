from sqlalchemy import Column, Integer, String, Date

from app.models.model import BGBModel


class LedgerExpense(BGBModel):
    id = Column(String, primary_key=True)  # 고유 ID
    
    transaction_date = Column(Date, index=True)  # 거래일 (지출일자)
    
    payment_method = Column(String)  # 결제 수단 (카드명)
    
    expense_type = Column(String)  # 지출 카테고리
    expense_detail_type = Column(String)  # 지출 세부 카테고리
    
    expense_amount = Column(Integer)  # 지출 금액
    expense_unit = Column(String)  # 지출 단위
    expense_merchant_name = Column(String)  # 가맹점/거래처
    
    note = Column(String)  # 비고 (지출 내용)
