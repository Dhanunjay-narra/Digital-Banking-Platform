"""Tests for Wallet Top-up, Withdraw, and UPI Simulator."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finx_platform.common.database import Base
from services.accounts.models import BankAccount
from services.wallet.service import wallet_service
from services.wallet.schemas import WalletTopupRequest, WalletWithdrawRequest
from services.upi.service import upi_service
from services.upi.schemas import UPISendRequest, QRCodeGenerateRequest


@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)
    session = TestingSession()

    acc = BankAccount(
        customer_id="cust_test_1",
        account_number="10009999",
        account_type="SAVINGS",
        currency="INR",
        status="ACTIVE",
        ledger_account_code="2000",
        available_balance=25000.0,
        branch_ifsc="FINX0001"
    )
    session.add(acc)
    session.commit()

    yield session
    session.close()


def test_wallet_topup_and_withdraw(db_session):
    wallet = wallet_service.get_or_create_wallet(db_session, "cust_test_1")
    initial_bal = wallet.balance

    # Top-up ₹3,000 from Bank Account
    wallet = wallet_service.top_up_wallet(db_session, "cust_test_1", WalletTopupRequest(
        source_bank_account="10009999",
        amount=3000.0
    ))
    assert wallet.balance == initial_bal + 3000.0

    # Withdraw ₹1,000 to Bank Account
    wallet = wallet_service.withdraw_to_bank(db_session, "cust_test_1", WalletWithdrawRequest(
        destination_bank_account="10009999",
        amount=1000.0
    ))
    assert wallet.balance == initial_bal + 2000.0


def test_upi_profile_and_qr_generation(db_session):
    profile = upi_service.get_or_create_profile(db_session, "cust_test_1", "10009999")
    assert "@finx" in profile.vpa_address

    qr_data = upi_service.generate_qr(db_session, "cust_test_1", QRCodeGenerateRequest(amount=500.0, note="Coffee"))
    assert "upi://pay" in qr_data["qr_payload"]
    assert "am=500.00" in qr_data["qr_payload"]
