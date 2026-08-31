"""Fraud Engine Pydantic Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class FraudEvaluationRequest(BaseModel):
    customer_id: str
    transaction_ref: str
    amount: float
    channel: str = "WEB"
    ip_address: Optional[str] = "127.0.0.1"
    device_id: Optional[str] = "dev-chrome-101"
    destination_account: str


class FraudEvaluationResponse(BaseModel):
    transaction_ref: str
    risk_score: float
    risk_decision: str
    triggered_rules: List[str]
    alert_id: Optional[str] = None


class FraudAlertResponse(BaseModel):
    id: str
    transaction_ref: str
    customer_id: str
    risk_score: float
    risk_decision: str
    status: str
    triggered_rules: str
    created_at: datetime

    class Config:
        from_attributes = True
