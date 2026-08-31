"""Merchant Pydantic Schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class MerchantCreateRequest(BaseModel):
    business_name: str
    business_type: str = "ECOMMERCE"
    contact_email: str
    contact_phone: str
    settlement_account_number: str
    settlement_ifsc: Optional[str] = "FINX0001001"


class MerchantResponse(BaseModel):
    id: str
    merchant_code: str
    business_name: str
    business_type: str
    contact_email: str
    contact_phone: str
    settlement_account_number: str
    mdr_rate_percent: float
    status: str
    api_key: str
    vpa_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SettlementResponse(BaseModel):
    id: str
    settlement_ref: str
    gross_volume: float
    fee_deducted: float
    net_settled_amount: float
    status: str
    utr_number: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
