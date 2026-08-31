"""KYC Domain Pydantic Schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class KYCSubmitRequest(BaseModel):
    document_type: str = "AADHAAR"
    document_number: str = Field(..., min_length=4)
    pan_number: str = Field(..., min_length=10, max_length=10)
    full_name: str
    date_of_birth: str
    annual_income: float = 1000000.0


class PANVerifyRequest(BaseModel):
    pan_number: str
    name_as_per_pan: str


class BankVerifyRequest(BaseModel):
    account_number: str
    ifsc_code: str
    beneficiary_name: str


class KYCResponse(BaseModel):
    id: str
    customer_id: str
    status: str
    kyc_level: str
    document_type: str
    pan_verified: bool
    bank_verified: bool
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True
