"""Dispute & Chargeback Management Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class Dispute(Base, TimestampMixin):
    __tablename__ = "disputes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dispute_reference = Column(String(50), unique=True, index=True, nullable=False)
    transaction_ref = Column(String(100), index=True, nullable=False)
    customer_id = Column(String(36), nullable=False, index=True)
    disputed_amount = Column(Float, nullable=False)
    reason = Column(String(255), nullable=False)
    evidence_text = Column(Text, nullable=True)
    status = Column(String(30), default="OPEN")  # OPEN, UNDER_REVIEW, WON, LOST, REFUNDED
    resolution_notes = Column(Text, nullable=True)
