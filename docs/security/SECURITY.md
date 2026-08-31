# Security & Compliance Framework

## 1. Encryption & Tokenization
- Sensitive data at rest (PAN, CVV, Card Numbers) is encrypted using reversible AES-256 field-level encryption.
- Passwords are salted and hashed using bcrypt (10 rounds).
- JWT access tokens use HMAC-SHA256 with 24-hour expiration in sandbox.

## 2. RBAC System
- 13 distinct roles with principle of least privilege:
  `SUPER_ADMIN`, `BANK_ADMIN`, `OPERATIONS_ADMIN`, `CUSTOMER_SUPPORT`, `FINANCE_OFFICER`, `LOAN_OFFICER`, `RISK_ANALYST`, `FRAUD_ANALYST`, `COMPLIANCE_OFFICER`, `MERCHANT_ADMIN`, `AUDITOR`, `REPORTING_USER`, `CUSTOMER`.

## 3. Real-Time Risk & Fraud Rules
- Anomaly detection on transaction amounts.
- Tor/Proxy high-risk IP blocking.
- Sanctions screening against OFAC & UN watchlists.
- Mandatory SAR reporting for suspicious volume clustering.
