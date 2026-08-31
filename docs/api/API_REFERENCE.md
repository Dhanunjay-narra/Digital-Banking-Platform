# FinXCore API Reference

The platform provides unified, versioned RESTful APIs on `/api/v1`:

- `/api/v1/auth`: Registration, Login, MFA, Passwordless OTP, Devices, Sessions.
- `/api/v1/customers`: Customer 360 profile, Beneficiaries, Nominees.
- `/api/v1/kyc`: Identity verification, PAN check, Penny-drop bank check.
- `/api/v1/accounts`: Savings, Current, Salary accounts opening, freeze/unfreeze.
- `/api/v1/ledger`: Chart of Accounts, Journal entries, Trial balance.
- `/api/v1/transactions`: Core transaction engine, reversals, history.
- `/api/v1/transfers`: Internal & external IMPS/NEFT transfers.
- `/api/v1/wallets`: Digital wallet top-up, withdrawal, ledger sync.
- `/api/v1/upi`: UPI rail simulator (@finx), dynamic QR generator, collect requests.
- `/api/v1/payments`: Merchant payment gateway orders, capture, refund.
- `/api/v1/cards`: RuPay virtual cards, PIN management, dynamic channel controls.
- `/api/v1/merchants`: Merchant profiles, settlements, terminal keys.
- `/api/v1/loans`: Loan product catalog, underwriting, reducing balance EMI schedule.
- `/api/v1/credit`: 300-900 Credit score engine, simulator.
- `/api/v1/investments`: Mutual funds, ETF, Gold holdings, SIP plans.
- `/api/v1/insurance`: Health, Term life quotes, Policy issuance, Claims.
- `/api/v1/expenses`: PFM expense tracking, auto-categorization, budgets.
- `/api/v1/bills`: Biller directory, bill pay.
- `/api/v1/fraud`: Real-time risk evaluation engine, alert resolution.
- `/api/v1/compliance`: Sanctions screening, PEP detection, SAR filing.
- `/api/v1/accounting`: Profit & Loss statement, Balance Sheet.
- `/api/v1/pricing`: Dynamic fee calculation with GST.
- `/api/v1/reconciliation`: Multi-rail 4-way automated matching.
- `/api/v1/disputes`: Chargeback and dispute lifecycle.
- `/api/v1/notifications`: Multi-channel notification dispatcher.
- `/api/v1/recommendations`: AI Financial Intelligence & Health score.
- `/api/v1/analytics`: Real-time KPIs & metrics.
- `/api/v1/reporting`: CSV & JSON statement exports.
- `/api/v1/admin`: Back-office overview & audit logs.
