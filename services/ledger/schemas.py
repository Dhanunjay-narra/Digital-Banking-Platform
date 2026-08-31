"""Double-Entry Ledger Pydantic Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PostingCreate(BaseModel):
    account_code: str
    entry_type: str = Field(..., pattern="^(DEBIT|CREDIT)$")
    amount: float = Field(..., gt=0)
    description: Optional[str] = None


class JournalEntryCreate(BaseModel):
    transaction_id: str
    description: str
    currency: str = "INR"
    postings: List[PostingCreate]


class LedgerAccountCreate(BaseModel):
    account_code: str
    account_name: str
    account_type: str = Field(..., pattern="^(ASSET|LIABILITY|EQUITY|REVENUE|EXPENSE)$")
    currency: str = "INR"
    description: Optional[str] = None


class LedgerAccountResponse(BaseModel):
    id: str
    account_code: str
    account_name: str
    account_type: str
    currency: str
    balance: float
    description: Optional[str]

    class Config:
        from_attributes = True


class TrialBalanceItem(BaseModel):
    account_code: str
    account_name: str
    account_type: str
    debit_balance: float
    credit_balance: float


class TrialBalanceResponse(BaseModel):
    items: List[TrialBalanceItem]
    total_debits: float
    total_credits: float
    is_balanced: bool
    generated_at: datetime
