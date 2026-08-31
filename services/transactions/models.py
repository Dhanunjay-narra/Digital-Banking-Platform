"""Core Transaction Engine Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class TransactionStatus(str, Enum):
    INITIATED = "INITIATED"
    VALIDATING = "VALIDATING"
    AUTHORIZED = "AUTHORIZED"
    PROCESSING = "PROCESSING"
    POSTED = "POSTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class TransactionType(str, Enum):
    INTERNAL_TRANSFER = "INTERNAL_TRANSFER"
    EXTERNAL_TRANSFER = "EXTERNAL_TRANSFER"
    UPI_PAYMENT = "UPI_PAYMENT"
    MERCHANT_PAYMENT = "MERCHANT_PAYMENT"
    WALLET_TOPUP = "WALLET_TOPUP"
    WALLET_WITHDRAWAL = "WALLET_WITHDRAWAL"
    CARD_PURCHASE = "CARD_PURCHASE"
    LOAN_DISBURSEMENT = "LOAN_DISBURSEMENT"
    LOAN_REPAYMENT = "LOAN_REPAYMENT"
    INVESTMENT_BUY = "INVESTMENT_BUY"
    INSURANCE_PREMIUM = "INSURANCE_PREMIUM"
    FEE_CHARGE = "FEE_CHARGE"
    REVERSAL = "REVERSAL"


class FinancialTransaction(Base, TimestampMixin):
    __tablename__ = "financial_transactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transaction_reference = Column(String(50), unique=True, index=True, nullable=False)
    idempotency_key = Column(String(100), unique=True, index=True, nullable=True)
    source_account = Column(String(50), index=True, nullable=False)
    destination_account = Column(String(50), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    fee_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    channel = Column(String(50), default="WEB")  # WEB, MOBILE, UPI, POS, ATM, API
    status = Column(String(30), default=TransactionStatus.INITIATED.value, nullable=False, index=True)
    description = Column(String(255), nullable=False)
    failure_reason = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)
