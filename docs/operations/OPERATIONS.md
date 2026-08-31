# Operations & Runbooks

## 1. Startup & Service Execution
```bash
# Start backend and web portal
python start_platform.py
```

## 2. Running Test Suite
```bash
pytest tests/
```

## 3. Daily Multi-Rail Reconciliation Runbook
Trigger automated 4-way matching between Core Banking, Payment Gateway, Switching Rail, and General Ledger via API:
```bash
POST /api/v1/reconciliation/run
```
Any detected discrepancies are flagged as breaks for finance operations review.
