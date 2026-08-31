"""Bills & Recurring Payments Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from platform.common.database import Base
from platform.common.base_model import generate_uuid, TimestampMixin


class BillerCategory(str, Enum):
    ELECTRICITY = "ELECTRICITY"
    WATER = "WATER"
    MOBILE_POSTPAID = "MOBILE_POSTPAID"
    BROADBAND = "BROADBAND"
    DTH = "DTH"
    FASTAG = "FASTAG"
    CREDIT_CARD = "CREDIT_CARD"


class CustomerBill(Base, TimestampMixin):
    __tablename__ = "customer_bills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    biller_name = Column(String(100), nullable=False)
    biller_category = Column(String(50), default=BillerCategory.ELECTRICITY.value, nullable=False)
    consumer_number = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(String(30), default="UNPAID")  # UNPAID, PAID, OVERDUE
    auto_pay_enabled = Column(Boolean, default=False)
    paid_at = Column(DateTime, nullable=True)
