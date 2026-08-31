"""UPI Rail Simulator Pydantic Schemas."""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class VPARegisterRequest(BaseModel):
    custom_handle: str = Field(..., min_length=3, max_length=30)
    linked_account_number: str
    upi_pin: str = Field(..., min_length=4, max_length=6)


class UPISendRequest(BaseModel):
    recipient_vpa: str
    amount: float = Field(..., gt=0)
    remarks: Optional[str] = "UPI Payment"
    upi_pin: Optional[str] = "1234"


class UPICollectCreateRequest(BaseModel):
    payer_vpa: str
    amount: float = Field(..., gt=0)
    remarks: Optional[str] = "UPI Collect Request"


class UPIPayCollectRequest(BaseModel):
    collect_request_id: str
    upi_pin: str = "1234"


class QRCodeGenerateRequest(BaseModel):
    amount: Optional[float] = None
    note: Optional[str] = "FinX UPI QR"


class UPIProfileResponse(BaseModel):
    id: str
    customer_id: str
    vpa_address: str
    linked_account_number: str
    daily_limit: float
    is_active: bool
    qr_payload: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UPITransactionResponse(BaseModel):
    success: bool
    transaction_id: str
    reference_number: str
    payer_vpa: str
    payee_vpa: str
    amount: float
    status: str
    timestamp: datetime
