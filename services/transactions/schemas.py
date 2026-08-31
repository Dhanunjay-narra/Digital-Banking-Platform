"""Transaction Engine Pydantic Schemas."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class TransactionInitiateRequest(BaseModel):
    source_account: str
    destination_account: str
    amount: float = Field(..., gt=0)
    currency: str = "INR"
    transaction_type: str = "INTERNAL_TRANSFER"
    channel: str = "WEB"
    description: str
    idempotency_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TransactionResponse(BaseModel):
    id: str
    transaction_reference: str
    source_account: str
    destination_account: str
    amount: float
    currency: str
    fee_amount: float
    status: str
    transaction_type: str
    channel: str
    description: str
    created_at: datetime
    failure_reason: Optional[str] = None

    class Config:
        from_attributes = True
