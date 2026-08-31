"""Credit Scoring Engine Pydantic Schemas."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ScoreSimulationRequest(BaseModel):
    repay_all_credit_cards: bool = False
    new_loan_amount: Optional[float] = None
    miss_one_payment: bool = False


class CreditScoreResponse(BaseModel):
    customer_id: str
    score: int
    credit_grade: str
    on_time_payment_pct: float
    credit_utilization_pct: float
    total_active_accounts: int
    credit_history_years: float
    recent_hard_inquiries: int
    recommended_credit_limit: float
    factors: Dict[str, str]

    class Config:
        from_attributes = True
