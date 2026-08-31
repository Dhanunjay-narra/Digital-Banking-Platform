"""Insurance Pydantic Schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class InsuranceQuoteRequest(BaseModel):
    policy_type: str = Field("HEALTH", pattern="^(HEALTH|TERM_LIFE|MOTOR|TRAVEL)$")
    sum_insured: float = Field(..., gt=10000)
    age: int = Field(30, ge=18, le=80)


class PolicyBuyRequest(BaseModel):
    policy_type: str
    plan_name: str
    sum_insured: float
    annual_premium: float
    source_account_number: Optional[str] = "100019283746"


class ClaimCreateRequest(BaseModel):
    policy_id: str
    claim_amount: float = Field(..., gt=0)
    reason: str


class InsurancePolicyResponse(BaseModel):
    id: str
    policy_number: str
    policy_type: str
    plan_name: str
    sum_insured: float
    annual_premium: float
    status: str
    start_date: datetime
    expiry_date: datetime

    class Config:
        from_attributes = True
