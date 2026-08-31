"""Tests for Authoritative Double-Entry Financial Ledger Invariants."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finx_platform.common.database import Base
from finx_platform.common.exceptions import UnbalancedLedgerException
from services.ledger.service import ledger_service
from services.ledger.schemas import JournalEntryCreate, PostingCreate


@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)
    session = TestingSession()
    ledger_service.initialize_chart_of_accounts(session)
    yield session
    session.close()


def test_balanced_journal_entry_success(db_session):
    req = JournalEntryCreate(
        transaction_id="TXN-TEST-100",
        description="Transfer from Customer A to Customer B",
        currency="INR",
        postings=[
            PostingCreate(account_code="2000", entry_type="DEBIT", amount=1500.0, description="Debit A"),
            PostingCreate(account_code="2010", entry_type="CREDIT", amount=1500.0, description="Credit B")
        ]
    )
    journal = ledger_service.post_journal_entry(db_session, req)
    assert journal.id is not None
    assert journal.total_debit == 1500.0
    assert journal.total_credit == 1500.0
    assert journal.status == "POSTED"


def test_unbalanced_journal_entry_fails_cleanly(db_session):
    req = JournalEntryCreate(
        transaction_id="TXN-UNBALANCED",
        description="Unbalanced Fraudulent Entry",
        currency="INR",
        postings=[
            PostingCreate(account_code="2000", entry_type="DEBIT", amount=1000.0),
            PostingCreate(account_code="2010", entry_type="CREDIT", amount=800.0)  # Difference of 200!
        ]
    )
    with pytest.raises(UnbalancedLedgerException) as exc_info:
        ledger_service.post_journal_entry(db_session, req)
    assert "unbalanced" in str(exc_info.value).lower()


def test_trial_balance_is_balanced(db_session):
    tb = ledger_service.get_trial_balance(db_session)
    assert tb.is_balanced is True
    assert tb.total_debits == tb.total_credits
