"""Tests for Loans Amortization, Credit Engine, Fraud & Compliance."""

import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finx_platform.common.database import Base
from finx_platform.common.math_utils import calculate_emi
from services.loans.service import loan_service
from services.loans.schemas import LoanApplyRequest
from services.credit.service import credit_engine
from services.credit.schemas import ScoreSimulationRequest
from services.fraud.service import fraud_engine
from services.fraud.schemas import FraudEvaluationRequest
from services.compliance.service import compliance_service
from services.compliance.schemas import SanctionsCheckRequest


@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)
    session = TestingSession()
    yield session
    session.close()


def test_emi_calculation_formula():
    principal = Decimal("100000.00")
    rate = Decimal("12.0")
    tenure = 12
    emi = calculate_emi(principal, rate, tenure)
    # Expected EMI for 100k at 12% for 12 months is ~8884.88
    assert float(emi) == 8884.88


def test_credit_scoring_and_simulation(db_session):
    profile = credit_engine.get_or_calculate_profile(db_session, "cust_sim_1")
    assert 300 <= profile.score <= 900

    sim = credit_engine.simulate_score(db_session, "cust_sim_1", ScoreSimulationRequest(repay_all_credit_cards=True))
    assert sim["simulated_score"] >= profile.score


def test_fraud_anomaly_detection_rules(db_session):
    # Low amount, normal IP -> ALLOW
    res_low = fraud_engine.evaluate_risk(db_session, FraudEvaluationRequest(
        customer_id="c1",
        transaction_ref="TXN-NORMAL",
        amount=500.0,
        destination_account="10002222"
    ))
    assert res_low.risk_decision == "ALLOW"

    # High amount + Tor IP -> BLOCK
    res_high = fraud_engine.evaluate_risk(db_session, FraudEvaluationRequest(
        customer_id="c1",
        transaction_ref="TXN-FRAUD",
        amount=900000.0,
        ip_address="185.220.101.5",
        destination_account="mule_account_99"
    ))
    assert res_high.risk_decision == "BLOCK"
    assert res_high.risk_score >= 70.0


def test_sanctions_screening_match(db_session):
    res_clean = compliance_service.screen_individual(db_session, SanctionsCheckRequest(full_name="Dhanunjay Narra"))
    assert res_clean.is_matched is False

    res_sanctioned = compliance_service.screen_individual(db_session, SanctionsCheckRequest(full_name="Viktor Bout"))
    assert res_sanctioned.is_matched is True
    assert res_sanctioned.action_required == "BLOCK_AND_REPORT"
