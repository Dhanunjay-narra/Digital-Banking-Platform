"""Double-Entry Financial Ledger Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Integer, Index
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class AccountType(str, Enum):
    ASSET = "ASSET"          # Cash, Bank reserve, Loans receivable, Wallet reserve
    LIABILITY = "LIABILITY"  # Customer deposits, Merchant payables, Suspense
    EQUITY = "EQUITY"        # Capital, Retained earnings
    REVENUE = "REVENUE"      # Transaction fees, Interchange, Interest income
    EXPENSE = "EXPENSE"      # Cashbacks, Operating costs, Gateway fees


class EntryType(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class LedgerAccount(Base, TimestampMixin):
    """Core Chart of Accounts item."""
    __tablename__ = "ledger_accounts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    account_code = Column(String(50), unique=True, index=True, nullable=False)
    account_name = Column(String(150), nullable=False)
    account_type = Column(String(30), nullable=False)  # ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    currency = Column(String(10), default="INR", nullable=False)
    balance = Column(Float, default=0.0, nullable=False)  # Authoritative derived / cached ledger balance
    description = Column(String(255), nullable=True)

    postings = relationship("LedgerPosting", back_populates="ledger_account")


class JournalEntry(Base, TimestampMixin):
    """Immutable Journal Entry containing balanced debits and credits."""
    __tablename__ = "journal_entries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    entry_number = Column(String(50), unique=True, index=True, nullable=False)
    transaction_id = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    total_debit = Column(Float, nullable=False)
    total_credit = Column(Float, nullable=False)
    status = Column(String(30), default="POSTED", nullable=False)  # POSTED, REVERSED

    postings = relationship("LedgerPosting", back_populates="journal_entry", cascade="all, delete-orphan")


class LedgerPosting(Base, TimestampMixin):
    """Individual debit or credit posting line."""
    __tablename__ = "ledger_postings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    journal_entry_id = Column(String(36), ForeignKey("journal_entries.id"), nullable=False, index=True)
    ledger_account_id = Column(String(36), ForeignKey("ledger_accounts.id"), nullable=False, index=True)
    entry_type = Column(String(10), nullable=False)  # DEBIT or CREDIT
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)

    journal_entry = relationship("JournalEntry", back_populates="postings")
    ledger_account = relationship("LedgerAccount", back_populates="postings")
