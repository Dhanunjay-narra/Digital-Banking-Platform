"""UPI Rail Simulator Database Models."""

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class UPIProfile(Base, TimestampMixin):
    __tablename__ = "upi_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), unique=True, nullable=False, index=True)
    vpa_address = Column(String(100), unique=True, index=True, nullable=False)  # e.g., dhanunjay@finx
    linked_account_number = Column(String(30), nullable=False)
    upi_pin_hash = Column(String(255), nullable=False)
    daily_limit = Column(Float, default=100000.0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    qr_payload = Column(Text, nullable=True)


class UPICollectRequest(Base, TimestampMixin):
    __tablename__ = "upi_collect_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    requester_vpa = Column(String(100), nullable=False, index=True)
    payer_vpa = Column(String(100), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    remarks = Column(String(255), nullable=True)
    status = Column(String(30), default="PENDING")  # PENDING, APPROVED, REJECTED, EXPIRED
    transaction_ref = Column(String(100), nullable=True)
