"""Digital Wallet Pydantic Schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class WalletTopupRequest(BaseModel):
    source_bank_account: str
    amount: float = Field(..., gt=0)


class WalletWithdrawRequest(BaseModel):
    destination_bank_account: str
    amount: float = Field(..., gt=0)


class WalletTransferRequest(BaseModel):
    recipient_phone_or_wallet: str
    amount: float = Field(..., gt=0)
    remarks: Optional[str] = "P2P Wallet Transfer"


class WalletResponse(BaseModel):
    id: str
    customer_id: str
    wallet_number: str
    balance: float
    currency: str
    status: str
    daily_limit: float
    created_at: datetime

    class Config:
        from_attributes = True


class WalletTransactionResponse(BaseModel):
    id: str
    transaction_type: str
    amount: float
    balance_after: float
    description: str
    reference_id: str
    created_at: datetime

    class Config:
        from_attributes = True
