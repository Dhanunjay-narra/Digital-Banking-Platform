"""Banking Accounts Pydantic Schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class AccountCreateRequest(BaseModel):
    account_type: str = Field("SAVINGS", pattern="^(SAVINGS|CURRENT|SALARY|VIRTUAL)$")
    currency: str = "INR"
    initial_deposit: float = Field(5000.0, ge=0)


class AccountFreezeRequest(BaseModel):
    account_number: str
    reason: str


class AccountResponse(BaseModel):
    id: str
    customer_id: str
    account_number: str
    account_type: str
    currency: str
    status: str
    available_balance: float
    hold_balance: float
    minimum_balance: float
    interest_rate_percent: float
    branch_ifsc: str
    created_at: datetime

    class Config:
        from_attributes = True
