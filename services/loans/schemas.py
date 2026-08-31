"""Loans Pydantic Schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class LoanApplyRequest(BaseModel):
    loan_type: str = Field("PERSONAL", pattern="^(PERSONAL|HOME|AUTO|EDUCATION|BUSINESS)$")
    amount: float = Field(..., gt=1000)
    tenure_months: int = Field(..., ge=6, le=360)
    disbursement_account_number: Optional[str] = None


class LoanUnderwriteDecisionRequest(BaseModel):
    application_id: str
    decision: str = Field(..., pattern="^(APPROVE|REJECT)$")
    notes: Optional[str] = "Approved based on credit evaluation"


class LoanRepayRequest(BaseModel):
    loan_id: str
    installment_number: int
    amount: float
    source_account_number: str


class LoanRepaymentItem(BaseModel):
    installment_number: int
    due_date: datetime
    principal_component: float
    interest_component: float
    total_installment_amount: float
    status: str

    class Config:
        from_attributes = True


class LoanResponse(BaseModel):
    id: str
    application_number: str
    customer_id: str
    loan_type: str
    requested_amount: float
    tenure_months: int
    interest_rate_annual: float
    monthly_emi: float
    status: str
    credit_score_at_application: int
    created_at: datetime

    class Config:
        from_attributes = True
