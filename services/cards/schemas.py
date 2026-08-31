"""Cards Management Pydantic Schemas."""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CardIssueRequest(BaseModel):
    card_type: str = Field("VIRTUAL", pattern="^(VIRTUAL|DEBIT|PREPAID|CREDIT)$")
    card_network: str = Field("RUPAY", pattern="^(RUPAY|VISA|MASTERCARD)$")
    cardholder_name: str
    pin: Optional[str] = "1234"


class CardPINSetRequest(BaseModel):
    card_id: str
    old_pin: Optional[str] = None
    new_pin: str = Field(..., min_length=4, max_length=4)


class CardControlsUpdateRequest(BaseModel):
    online_enabled: Optional[bool] = None
    atm_enabled: Optional[bool] = None
    pos_enabled: Optional[bool] = None
    contactless_enabled: Optional[bool] = None
    international_enabled: Optional[bool] = None
    daily_limit: Optional[float] = None


class CardResponse(BaseModel):
    id: str
    customer_id: str
    card_number_masked: str
    card_type: str
    card_network: str
    expiry_month: str
    expiry_year: str
    cardholder_name: str
    status: str
    online_enabled: bool
    atm_enabled: bool
    pos_enabled: bool
    contactless_enabled: bool
    international_enabled: bool
    daily_limit: float
    created_at: datetime

    class Config:
        from_attributes = True


class CardRevealResponse(BaseModel):
    id: str
    card_number: str
    cvv: str
    expiry: str
    cardholder_name: str
