"""Bills Pydantic Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BillPayRequest(BaseModel):
    bill_id: str
    source_account_number: Optional[str] = "100019283746"


class BillResponse(BaseModel):
    id: str
    biller_name: str
    biller_category: str
    consumer_number: str
    amount: float
    due_date: datetime
    status: str
    auto_pay_enabled: bool

    class Config:
        from_attributes = True
