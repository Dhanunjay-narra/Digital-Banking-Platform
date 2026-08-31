"""Insurance Platform Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class PolicyType(str, Enum):
    HEALTH = "HEALTH"
    TERM_LIFE = "TERM_LIFE"
    MOTOR = "MOTOR"
    TRAVEL = "TRAVEL"


class InsurancePolicy(Base, TimestampMixin):
    __tablename__ = "insurance_policies"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    policy_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    policy_type = Column(String(30), default=PolicyType.HEALTH.value, nullable=False)
    plan_name = Column(String(150), nullable=False)
    sum_insured = Column(Float, nullable=False)
    annual_premium = Column(Float, nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False)  # ACTIVE, LAPSED, CLAIMED, EXPIRED
    start_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)


class InsuranceClaim(Base, TimestampMixin):
    __tablename__ = "insurance_claims"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    claim_number = Column(String(50), unique=True, index=True, nullable=False)
    policy_id = Column(String(36), ForeignKey("insurance_policies.id"), nullable=False, index=True)
    claim_amount = Column(Float, nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(String(30), default="SUBMITTED")  # SUBMITTED, UNDER_REVIEW, APPROVED, REJECTED, SETTLED
