"""Tests for Pricing Engine, Taxes, and Multi-Rail Reconciliation."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finx_platform.common.database import Base
from services.pricing.service import pricing_engine
from services.reconciliation.service import reconciliation_engine


@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)
    session = TestingSession()
    yield session
    session.close()


def test_mdr_fee_calculation():
    calc = pricing_engine.calculate_fee("MERCHANT_MDR", 10000.0)
    # 1.8% on 10,000 is 180 + 18% GST (32.40) = 212.40
    assert calc["base_fee"] == 180.0
    assert calc["gst_tax_18_pct"] == 32.4
    assert calc["total_charge"] == 212.4


def test_premium_customer_fee_waiver():
    calc_std = pricing_engine.calculate_fee("IMPS_TRANSFER", 25000.0, "RETAIL_STANDARD")
    calc_prem = pricing_engine.calculate_fee("IMPS_TRANSFER", 25000.0, "PREMIUM")
    assert calc_prem["net_fee"] < calc_std["net_fee"]
    assert calc_prem["discount_percent"] == 50.0


def test_reconciliation_engine_zero_breaks_on_clean_ledger(db_session):
    report = reconciliation_engine.run_reconciliation(db_session)
    assert report["status"] == "BALANCED"
    assert report["breaks_count"] == 0
