"""Bank Transfers Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class TransferRail(str, Enum):
    INTERNAL = "INTERNAL"
    IMPS = "IMPS"
    NEFT = "NEFT"
    RTGS = "RTGS"
    UPI = "UPI"


class BankTransfer(Base, TimestampMixin):
    __tablename__ = "bank_transfers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transfer_reference = Column(String(50), unique=True, index=True, nullable=False)
    source_account = Column(String(50), nullable=False, index=True)
    destination_account = Column(String(50), nullable=False, index=True)
    beneficiary_name = Column(String(150), nullable=False)
    destination_ifsc = Column(String(20), nullable=True)
    rail = Column(String(30), default=TransferRail.INTERNAL.value, nullable=False)
    amount = Column(Float, nullable=False)
    fee_amount = Column(Float, default=0.0, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    status = Column(String(30), default="COMPLETED", nullable=False)  # PENDING, COMPLETED, FAILED, SCHEDULED
    remarks = Column(String(255), nullable=True)
    utr_number = Column(String(50), unique=True, index=True, nullable=True)


class ScheduledTransfer(Base, TimestampMixin):
    __tablename__ = "scheduled_transfers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    source_account = Column(String(50), nullable=False)
    destination_account = Column(String(50), nullable=False)
    beneficiary_name = Column(String(150), nullable=False)
    amount = Column(Float, nullable=False)
    frequency = Column(String(30), default="MONTHLY")  # ONCE, DAILY, WEEKLY, MONTHLY
    next_execution_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
