"""Payment Gateway Pydantic Schemas."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PaymentOrderCreate(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = "INR"
    receipt: Optional[str] = None
    merchant_id: Optional[str] = "merch_demo_101"
    customer_email: Optional[str] = "customer@finxcore.com"
    customer_phone: Optional[str] = "+919876543210"
    notes: Optional[Dict[str, Any]] = None


class PaymentCaptureRequest(BaseModel):
    order_id: str
    amount: float
    payment_method: str = "UPI"  # UPI, CARD, NETBANKING, WALLET


class PaymentRefundRequest(BaseModel):
    order_id: str
    amount: float
    reason: Optional[str] = "Customer return"


class PaymentOrderResponse(BaseModel):
    id: str
    order_id: str
    merchant_id: str
    amount: float
    currency: str
    status: str
    payment_method: Optional[str]
    amount_captured: float
    amount_refunded: float
    created_at: datetime

    class Config:
        from_attributes = True
