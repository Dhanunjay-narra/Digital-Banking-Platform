"""Merchant Management Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class MerchantProfile(Base, TimestampMixin):
    __tablename__ = "merchants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    merchant_code = Column(String(50), unique=True, index=True, nullable=False)
    business_name = Column(String(150), nullable=False)
    business_type = Column(String(50), default="ECOMMERCE")  # RETAIL, ECOMMERCE, RESTAURANT, SERVICES
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(30), nullable=False)
    settlement_account_number = Column(String(50), nullable=False)
    settlement_ifsc = Column(String(20), default="FINX0001001")
    mdr_rate_percent = Column(Float, default=1.8)
    status = Column(String(30), default="ACTIVE")  # ACTIVE, PENDING_KYC, SUSPENDED
    api_key = Column(String(100), unique=True, nullable=False)
    vpa_address = Column(String(100), nullable=True)


class MerchantSettlement(Base, TimestampMixin):
    __tablename__ = "merchant_settlements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    settlement_ref = Column(String(50), unique=True, index=True, nullable=False)
    merchant_id = Column(String(36), ForeignKey("merchants.id"), nullable=False, index=True)
    gross_volume = Column(Float, nullable=False)
    fee_deducted = Column(Float, nullable=False)
    net_settled_amount = Column(Float, nullable=False)
    status = Column(String(30), default="SETTLED")  # PENDING, PROCESSING, SETTLED, FAILED
    utr_number = Column(String(50), nullable=True)
