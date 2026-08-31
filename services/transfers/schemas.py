"""Bank Transfers Pydantic Schemas."""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TransferInitiateRequest(BaseModel):
    source_account: str
    destination_account: str
    beneficiary_name: str
    destination_ifsc: Optional[str] = "FINX0001001"
    rail: str = Field("INTERNAL", pattern="^(INTERNAL|IMPS|NEFT|RTGS|UPI)$")
    amount: float = Field(..., gt=0)
    currency: str = "INR"
    remarks: Optional[str] = "Funds Transfer"
    idempotency_key: Optional[str] = None


class TransferResponse(BaseModel):
    id: str
    transfer_reference: str
    source_account: str
    destination_account: str
    beneficiary_name: str
    rail: str
    amount: float
    fee_amount: float
    status: str
    utr_number: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
