"""Comprehensive End-to-End Multi-Domain Banking Lifecycle Test."""

import pytest
from fastapi.testclient import TestClient
from finx_platform.api_gateway.main import app
from finx_platform.common.database import Base, engine, SessionLocal


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_complete_fintech_super_platform_flow(client):
    # 1. Health Ping
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"

    # 2. Authenticate Demo Customer
    login_res = client.post("/api/v1/auth/login", json={
        "email": "customer@finxcore.com",
        "password": "FinX@2026"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Retrieve Customer 360 View
    c360_res = client.get("/api/v1/customers/me", headers=headers)
    assert c360_res.status_code == 200
    c360_data = c360_res.json()
    assert "customer" in c360_data
    assert c360_data["credit_score"] >= 700

    # 4. Check Bank Accounts
    accs_res = client.get("/api/v1/accounts", headers=headers)
    assert accs_res.status_code == 200
    acc_list = accs_res.json()
    assert len(acc_list) >= 1
    acc_num = acc_list[0]["account_number"]

    # 5. Initiate IMPS Transfer & Verify Double-Entry Execution
    trf_res = client.post("/api/v1/transfers/execute", json={
        "source_account": acc_num,
        "destination_account": "200084736281",
        "beneficiary_name": "NexGen Retail",
        "rail": "IMPS",
        "amount": 2500.0,
        "remarks": "E2E Test Transfer"
    })
    assert trf_res.status_code == 200
    assert trf_res.json()["status"] == "COMPLETED"

    # 6. Retrieve Authoritative General Ledger Trial Balance
    tb_res = client.get("/api/v1/ledger/trial-balance")
    assert tb_res.status_code == 200
    tb_data = tb_res.json()
    assert tb_data["is_balanced"] is True

    # 7. Card Platform: Issue & Reveal Card
    card_res = client.get("/api/v1/cards", headers=headers)
    assert card_res.status_code == 200
    cards = card_res.json()
    assert len(cards) >= 1
    card_id = cards[0]["id"]

    reveal_res = client.get(f"/api/v1/cards/{card_id}/reveal", headers=headers)
    assert reveal_res.status_code == 200
    assert "cvv" in reveal_res.json()

    # 8. Merchant Payment Gateway: Create Order & Capture
    order_res = client.post("/api/v1/payments/orders", json={
        "amount": 1800.0,
        "currency": "INR",
        "merchant_id": "merch_demo_101"
    })
    assert order_res.status_code == 200
    order_id = order_res.json()["order_id"]

    capture_res = client.post("/api/v1/payments/capture", json={
        "order_id": order_id,
        "amount": 1800.0,
        "payment_method": "UPI"
    })
    assert capture_res.status_code == 200
    assert capture_res.json()["status"] == "CAPTURED"

    # 9. Loan Application with Amortization Schedule
    loan_res = client.post("/api/v1/loans/apply", headers=headers, json={
        "loan_type": "PERSONAL",
        "amount": 150000.0,
        "tenure_months": 18
    })
    assert loan_res.status_code == 200
    loan_id = loan_res.json()["id"]

    schedule_res = client.get(f"/api/v1/loans/{loan_id}/schedule")
    assert schedule_res.status_code == 200
    assert len(schedule_res.json()) == 18

    # 10. AI Financial Recommendations
    rec_res = client.get("/api/v1/recommendations", headers=headers)
    assert rec_res.status_code == 200
    assert "financial_health_score" in rec_res.json()
