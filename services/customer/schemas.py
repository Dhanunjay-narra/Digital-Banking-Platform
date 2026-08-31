"""Customer Domain Pydantic Schemas."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AddressCreate(BaseModel):
    address_type: str = "CURRENT"
    street_line1: str
    street_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "India"
    is_primary: bool = True


class BeneficiaryCreate(BaseModel):
    name: str
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    vpa_address: Optional[str] = None
    bank_name: Optional[str] = "FinX Bank"
    transfer_type: str = "INTERNAL"
    daily_limit: float = 100000.0


class NomineeCreate(BaseModel):
    name: str
    relationship_type: str
    date_of_birth: Optional[str] = None
    share_percentage: float = 100.0
    contact_number: Optional[str] = None


class CustomerCreate(BaseModel):
    pan_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    occupation: Optional[str] = "Software Professional"
    annual_income: float = 1200000.0
    customer_segment: str = "RETAIL_STANDARD"


class CustomerResponse(BaseModel):
    id: str
    user_id: str
    customer_segment: str
    customer_status: str
    pan_number: Optional[str]
    risk_rating: str
    annual_income: float
    created_at: datetime

    class Config:
        from_attributes = True


class Customer360Response(BaseModel):
    customer: CustomerResponse
    user: Dict[str, Any]
    kyc_status: str
    accounts: List[Dict[str, Any]]
    wallet_balance: float
    cards_count: int
    active_loans_count: int
    total_investments_value: float
    active_policies_count: int
    credit_score: int
    risk_profile: str
    recent_transactions: List[Dict[str, Any]]
