"""Digital Wallet Database Models."""

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class DigitalWallet(Base, TimestampMixin):
    __tablename__ = "digital_wallets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), unique=True, nullable=False, index=True)
    wallet_number = Column(String(30), unique=True, index=True, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False)  # ACTIVE, FROZEN, CLOSED
    daily_limit = Column(Float, default=50000.0, nullable=False)
    monthly_limit = Column(Float, default=200000.0, nullable=False)

    transactions = relationship("WalletTransaction", back_populates="wallet", cascade="all, delete-orphan")


class WalletTransaction(Base, TimestampMixin):
    __tablename__ = "wallet_transactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    wallet_id = Column(String(36), ForeignKey("digital_wallets.id"), nullable=False, index=True)
    transaction_type = Column(String(50), nullable=False)  # TOP_UP, WITHDRAWAL, P2P_TRANSFER, MERCHANT_PAY
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    reference_id = Column(String(100), index=True, nullable=False)

    wallet = relationship("DigitalWallet", back_populates="transactions")
