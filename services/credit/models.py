"""Credit Scoring Engine Database Models."""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class CreditProfile(Base, TimestampMixin):
    __tablename__ = "credit_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), unique=True, nullable=False, index=True)
    score = Column(Integer, default=750, nullable=False)
    credit_grade = Column(String(20), default="EXCELLENT", nullable=False)  # EXCELLENT, VERY_GOOD, GOOD, FAIR, POOR
    on_time_payment_pct = Column(Float, default=98.5)
    credit_utilization_pct = Column(Float, default=18.0)
    total_active_accounts = Column(Integer, default=4)
    credit_history_years = Column(Float, default=4.5)
    recent_hard_inquiries = Column(Integer, default=1)
    recommended_credit_limit = Column(Float, default=350000.0)
    last_pulled_at = Column(DateTime, nullable=True)
