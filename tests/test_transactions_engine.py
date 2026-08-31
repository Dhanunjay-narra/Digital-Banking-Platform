"""Tests for Core Transaction Engine and State Transitions."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finx_platform.common.database import Base
from finx_platform.common.exceptions import InsufficientFundsException
from services.accounts.models import BankAccount
from services.transactions.service import transaction_engine
from services.transactions.schemas import TransactionInitiateRequest
from services.transactions.models import TransactionStatus


@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)
    session = TestingSession()

    # Create test bank accounts
    acc1 = BankAccount(
        customer_id="cust_1",
        account_number="10001111",
        account_type="SAVINGS",
        currency="INR",
        status="ACTIVE",
        ledger_account_code="2000",
        available_balance=5000.0,
        branch_ifsc="FINX0001"
    )
    acc2 = BankAccount(
        customer_id="cust_2",
        account_number="10002222",
        account_type="SAVINGS",
        currency="INR",
        status="ACTIVE",
        ledger_account_code="2000",
        available_balance=1000.0,
        branch_ifsc="FINX0001"
    )
    session.add(acc1)
    session.add(acc2)
    session.commit()

    yield session
    session.close()


def test_successful_transaction_execution(db_session):
    req = TransactionInitiateRequest(
        source_account="10001111",
        destination_account="10002222",
        amount=1500.0,
        currency="INR",
        transaction_type="INTERNAL_TRANSFER",
        description="Test payment"
    )
    tx = transaction_engine.execute_transaction(db_session, req)
    assert tx.status == TransactionStatus.COMPLETED.value
    assert tx.amount == 1500.0

    acc1 = db_session.query(BankAccount).filter(BankAccount.account_number == "10001111").first()
    acc2 = db_session.query(BankAccount).filter(BankAccount.account_number == "10002222").first()
    assert acc1.available_balance == 3500.0
    assert acc2.available_balance == 2500.0


def test_insufficient_funds_fails_cleanly(db_session):
    req = TransactionInitiateRequest(
        source_account="10001111",
        destination_account="10002222",
        amount=50000.0,  # Exceeds 5000!
        currency="INR",
        transaction_type="INTERNAL_TRANSFER",
        description="Overdraft attempt"
    )
    with pytest.raises(InsufficientFundsException):
        transaction_engine.execute_transaction(db_session, req)
