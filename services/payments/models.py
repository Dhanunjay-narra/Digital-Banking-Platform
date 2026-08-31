"""Merchant Payment Gateway Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from platform.common.database import Base
from platform.common.base_model import generate_uuid, TimestampMixin


class PaymentStatus(str, Enum):
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED = "CAPTURED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    FAILED = "FAILED"


class PaymentOrder(Base, TimestampMixin):
    __tablename__ = "payment_orders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_id = Column(String(50), unique=True, index=True, nullable=False)
    merchant_id = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    receipt = Column(String(100), nullable=True)
    status = Column(String(30), default=PaymentStatus.CREATED.value, nullable=False)
    payment_method = Column(String(50), nullable=True)  # CARD, UPI, NETBANKING, WALLET
    amount_captured = Column(Float, default=0.0, nullable=False)
    amount_refunded = Column(Float, default=0.0, nullable=False)
    customer_email = Column(String(255), nullable=True)
    customer_phone = Column(String(30), nullable=True)
    notes_json = Column(Text, nullable=True)

    refunds = relationship("PaymentRefund", back_populates="order", cascade="all, delete-orphan")


class PaymentRefund(Base, TimestampMixin):
    __tablename__ = "payment_refunds"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    refund_id = Column(String(50), unique=True, index=True, nullable=False)
    order_id = Column(String(36), ForeignKey("payment_orders.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    status = Column(String(30), default="PROCESSED")
    reason = Column(String(255), nullable=True)

    order = relationship("PaymentOrder", back_populates="refunds")
