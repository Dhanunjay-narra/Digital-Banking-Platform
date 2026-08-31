"""Cards Management Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class CardType(str, Enum):
    DEBIT = "DEBIT"
    VIRTUAL = "VIRTUAL"
    PREPAID = "PREPAID"
    CREDIT = "CREDIT"


class PaymentCard(Base, TimestampMixin):
    __tablename__ = "payment_cards"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    card_number_masked = Column(String(30), nullable=False)
    card_number_encrypted = Column(String(255), nullable=False)
    card_type = Column(String(30), default="VIRTUAL", nullable=False)  # VIRTUAL, DEBIT, PREPAID
    card_network = Column(String(30), default="RUPAY", nullable=False)  # RUPAY, VISA, MASTERCARD
    expiry_month = Column(String(2), nullable=False)
    expiry_year = Column(String(4), nullable=False)
    cvv_encrypted = Column(String(255), nullable=False)
    cardholder_name = Column(String(150), nullable=False)
    pin_hash = Column(String(255), nullable=True)
    status = Column(String(30), default="ACTIVE", nullable=False)  # ACTIVE, BLOCKED, EXPIRED, INACTIVE

    # Channel Controls
    online_enabled = Column(Boolean, default=True)
    atm_enabled = Column(Boolean, default=True)
    pos_enabled = Column(Boolean, default=True)
    contactless_enabled = Column(Boolean, default=True)
    international_enabled = Column(Boolean, default=False)
    daily_limit = Column(Float, default=50000.0)
