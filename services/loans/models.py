"""Loan Management Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from platform.common.database import Base
from platform.common.base_model import generate_uuid, TimestampMixin


class LoanType(str, Enum):
    PERSONAL = "PERSONAL"
    HOME = "HOME"
    AUTO = "AUTO"
    EDUCATION = "EDUCATION"
    BUSINESS = "BUSINESS"


class LoanStatus(str, Enum):
    APPLIED = "APPLIED"
    UNDERWRITING = "UNDERWRITING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DISBURSED = "DISBURSED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    DEFAULTED = "DEFAULTED"


class LoanApplication(Base, TimestampMixin):
    __tablename__ = "loan_applications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    application_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    loan_type = Column(String(30), default=LoanType.PERSONAL.value, nullable=False)
    requested_amount = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    interest_rate_annual = Column(Float, nullable=False)  # e.g., 10.5%
    monthly_emi = Column(Float, nullable=False)
    status = Column(String(30), default=LoanStatus.APPLIED.value, nullable=False)
    disbursed_account_number = Column(String(30), nullable=True)
    credit_score_at_application = Column(Integer, default=750)
    underwriter_notes = Column(Text, nullable=True)
    rejection_reason = Column(String(255), nullable=True)
    disbursed_at = Column(DateTime, nullable=True)

    repayments = relationship("LoanRepayment", back_populates="loan", cascade="all, delete-orphan")


class LoanRepayment(Base, TimestampMixin):
    __tablename__ = "loan_repayments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    loan_id = Column(String(36), ForeignKey("loan_applications.id"), nullable=False, index=True)
    installment_number = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=False)
    principal_component = Column(Float, nullable=False)
    interest_component = Column(Float, nullable=False)
    total_installment_amount = Column(Float, nullable=False)
    status = Column(String(30), default="PENDING")  # PENDING, PAID, OVERDUE
    paid_at = Column(DateTime, nullable=True)
    payment_reference = Column(String(100), nullable=True)

    loan = relationship("LoanApplication", back_populates="repayments")
