"""Banking Accounts Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from platform.common.database import Base
from platform.common.base_model import generate_uuid, TimestampMixin


class AccountClass(str, Enum):
    SAVINGS = "SAVINGS"
    CURRENT = "CURRENT"
    SALARY = "SALARY"
    VIRTUAL = "VIRTUAL"


class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DORMANT = "DORMANT"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


class BankAccount(Base, TimestampMixin):
    __tablename__ = "bank_accounts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    account_number = Column(String(30), unique=True, index=True, nullable=False)
    account_type = Column(String(30), default="SAVINGS", nullable=False)  # SAVINGS, CURRENT, SALARY, VIRTUAL
    currency = Column(String(10), default="INR", nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False)  # ACTIVE, FROZEN, CLOSED
    ledger_account_code = Column(String(50), nullable=False)
    available_balance = Column(Float, default=0.0, nullable=False)
    hold_balance = Column(Float, default=0.0, nullable=False)
    minimum_balance = Column(Float, default=1000.0, nullable=False)
    interest_rate_percent = Column(Float, default=4.0, nullable=False)
    branch_ifsc = Column(String(20), default="FINX0001001", nullable=False)

    holds = relationship("AccountHold", back_populates="account", cascade="all, delete-orphan")


class AccountHold(Base, TimestampMixin):
    __tablename__ = "account_holds"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    account_id = Column(String(36), ForeignKey("bank_accounts.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(String(30), default="ACTIVE")  # ACTIVE, RELEASED, CAPTURED
    expires_at = Column(DateTime, nullable=True)

    account = relationship("BankAccount", back_populates="holds")
