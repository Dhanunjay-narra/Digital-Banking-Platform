"""Real-time Fraud & Risk Engine Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from platform.common.database import Base
from platform.common.base_model import generate_uuid, TimestampMixin


class RiskDecision(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


class FraudAlert(Base, TimestampMixin):
    __tablename__ = "fraud_alerts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transaction_ref = Column(String(100), index=True, nullable=False)
    customer_id = Column(String(36), nullable=False, index=True)
    risk_score = Column(Float, nullable=False)  # 0.0 to 100.0
    risk_decision = Column(String(20), default=RiskDecision.ALLOW.value, nullable=False)
    triggered_rules = Column(Text, nullable=False)  # JSON array of triggered rules
    status = Column(String(30), default="OPEN")  # OPEN, INVESTIGATING, RESOLVED_FALSE_POSITIVE, RESOLVED_CONFIRMED_FRAUD
    assigned_analyst = Column(String(100), nullable=True)
    resolution_notes = Column(Text, nullable=True)
