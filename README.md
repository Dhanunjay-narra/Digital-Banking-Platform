# FinXCore — Intelligent Digital Banking & Financial Super Platform

[![Build Status](https://img.shields.io/badge/Build-Passing-emerald)](https://github.com/Dhanunjay-narra/Digital-Banking-Platform)
[![Architecture](https://img.shields.io/badge/Architecture-Domain--Oriented%20Microservices-blue)](docs/architecture/ARCHITECTURE.md)
[![Double-Entry Ledger](https://img.shields.io/badge/Financial%20Ledger-Balanced%20Double--Entry-purple)](#10-double-entry-financial-ledger)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.110+-009688)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-FinXCore%20Proprietary-red)](LICENSE)

FinXCore is a production-grade, full-stack **FinTech & Digital Banking Super Platform** delivering complete unified banking, instant payment rails (UPI simulator), merchant payment gateway, double-entry financial ledger, credit scoring, automated loan underwriting, mutual funds/investments, insurance, real-time fraud detection, and multi-rail reconciliation.

---

## 1. High-Level Architecture

```
                         ┌─────────────────────────────────────────┐
                         │              Web & Mobile               │
                         │    Customer / Merchant / Admin Portals  │
                         └────────────────────┬────────────────────┘
                                              │
                                      API Gateway / WAF
                                              │
                         ┌────────────────────▼────────────────────┐
                         │           Identity & Security           │
                         │         IAM / MFA / RBAC (13 Roles)     │
                         └────────────────────┬────────────────────┘
                                              │
                 ┌────────────────────────────┼────────────────────────────┐
                 │                            │                            │
        ┌────────▼────────┐          ┌────────▼────────┐          ┌────────▼────────┐
        │ Customer Domain │          │ Banking Domain  │          │ Payment Domain  │
        │ • Customer 360  │          │ • Savings/Salary│          │ • UPI Simulator │
        │ • KYC / CDD / EDD          │ • Transaction SM│          │ • Gateway (MDR) │
        └────────┬────────┘          └────────┬────────┘          └────────┬────────┘
                 │                            │                            │
        ┌────────▼────────┐          ┌────────▼────────┐          ┌────────▼────────┐
        │  Wallet Domain  │          │   Card Domain   │          │ Merchant Domain │
        │ • Topup/Withdraw│          │ • RuPay Virtual │          │ • Settlements   │
        └────────┬────────┘          └────────┬────────┘          └────────┬────────┘
                 │                            │                            │
                 └────────────────────────────┼────────────────────────────┘
                                              │
                                   ┌──────────▼──────────┐
                                   │  Financial Ledger   │
                                   │ Double Entry Ledger │
                                   │ Σ Debits = Σ Credits│
                                   └──────────┬──────────┘
                                              │
        ┌─────────────────────────────────────┼─────────────────────────────────────┐
        │                                     │                                     │
 ┌──────▼───────┐                     ┌───────▼──────┐                     ┌───────▼──────┐
 │ Loan Engine  │                     │ Credit Score │                     │ Investments  │
 │ • Amortize   │                     │ • 300-900 Pt │                     │ • SIPs & P&L │
 └──────┬───────┘                     └───────┬──────┘                     └───────┬──────┘
        │                                     │                                     │
 ┌──────▼───────┐                     ┌───────▼──────┐                     ┌───────▼──────┐
 │ Insurance    │                     │  Fraud/Risk  │                     │  Analytics   │
 │ • Quotes     │                     │ • Real-time  │                     │ • Live KPIs  │
 └──────┬───────┘                     └───────┬──────┘                     └───────┬──────┘
        │                                     │                                     │
        └─────────────────────────────────────┼─────────────────────────────────────┘
                                              │
                                 ┌────────────▼────────────┐
                                 │ Compliance / Reporting  │
                                 │ AML, Sanctions, SARs    │
                                 └─────────────────────────┘
```

---

## 2. Key Modules & Capabilities

| Domain | Key Capabilities | Authoritative Owner |
|---|---|---|
| **Identity & IAM** | Registration, Passwordless OTP, MFA, Device Trust, Sessions, RBAC for 13 Roles | `services/identity` |
| **Customer & KYC** | Customer 360 Aggregator, Address management, Beneficiaries, Nominees, PAN/Bank Verification, CDD/EDD | `services/customer`, `services/kyc` |
| **Double-Entry Ledger** | Chart of Accounts, Invariant balanced debits and credits ($\sum \text{Debits} = \sum \text{Credits}$), Trial Balance | `services/ledger` |
| **Banking Accounts** | Savings, Current, Salary, Virtual Accounts, Interest Calculation, Account Holds/Freezes | `services/accounts` |
| **Transaction Engine** | Strict State Machine (`INITIATED` $\rightarrow$ `VALIDATING` $\rightarrow$ `AUTHORIZED` $\rightarrow$ `PROCESSING` $\rightarrow$ `POSTED` $\rightarrow$ `COMPLETED`), Idempotency, Concurrency Locks | `services/transactions` |
| **Money Movement** | IMPS, NEFT, RTGS, Scheduled & Recurring Transfers | `services/transfers` |
| **Digital Wallet** | Prepaid wallet, Top-up, Withdrawal, P2P Transfers, Ledger Escrow pool | `services/wallet` |
| **UPI Rail Simulator** | VPA (`@finx`), Send Money, Dynamic & Static QR generator (`upi://pay`), Collect requests | `services/upi` |
| **Payment Gateway** | Merchant orders, Tokenized Checkout, Capture, Full/Partial Refunds, MDR calculations | `services/payments` |
| **Card Platform** | RuPay Virtual/Debit/Prepaid cards, Luhn generator, CVV reveal, PIN setting, Dynamic controls (ATM, POS, Ecom, NFC) | `services/cards` |
| **Merchant Rail** | Merchant onboarding, T+0 settlements, Terminal keys, Merchant QR | `services/merchants` |
| **Loans & Credit** | Personal/Home/Auto loan products, Automated underwriting, Reducing balance EMI amortization, 300-900 Credit Score Engine | `services/loans`, `services/credit` |
| **Investments & Wealth**| Mutual funds, ETFs, Digital 24K Gold, Sovereign Bonds, SIP auto-debits, Portfolio P&L | `services/investments` |
| **Insurance** | Health, Term Life, Motor, Travel policies, Quote calculator, Policy issuance, Claims workflow | `services/insurance` |
| **Personal Finance** | Automatic transaction categorization, Income vs Expense tracking, Monthly budget limits, Recurring bills | `services/expenses`, `services/bills` |
| **Fraud & AML Risk** | Real-time risk scoring, Velocity anomaly rules, Tor/Proxy IP blocking, OFAC/UN Sanctions screening, SAR filing | `services/fraud`, `services/compliance` |
| **Operations & Accounting**| General Ledger, Profit & Loss statement, Balance Sheet, Multi-Rail 4-way automated reconciliation, Disputes & Chargebacks | `services/accounting`, `services/pricing`, `services/reconciliation`, `services/disputes` |
| **AI Intelligence** | Financial Health Score (0-100), Savings recommendations, Spending anomaly alerts | `services/recommendations`, `ml/` |

---

## 3. Quickstart & 1-Click Role Login

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/Dhanunjay-narra/Digital-Banking-Platform.git
cd Digital-Banking-Platform

# Install dependencies
pip install -r requirements.txt
```

### Run Platform & Web Portals
```bash
python start_platform.py
```
Open your browser at:
- **Interactive Banking Portals**: [http://localhost:8000](http://localhost:8000)
- **Interactive OpenAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint**: [http://localhost:8000/health](http://localhost:8000/health)

### 1-Click Pre-Seeded Test Credentials
The frontend includes a **1-Click Quick Persona Bar** at the top. You can instantly switch between:
- **Customer**: `customer@finxcore.com` / `FinX@2026` (Dhanunjay Narra - Pre-funded Savings ₹2,48,500, Wallet ₹18,500, Credit Score 782)
- **Merchant**: `merchant@finxcore.com` / `FinX@2026` (NexGen Retail - Payment Gateway Terminal, QR & Settlements)
- **Super Admin**: `superadmin@finxcore.com` / `FinX@2026` (Full Back-Office Access, Chart of Accounts, Fraud Console, Reconciliations)
- **Loan Officer**: `loan.officer@finxcore.com` / `FinX@2026` (Underwriting & Credit decisions)
- **Compliance Officer**: `compliance@finxcore.com` / `FinX@2026` (Sanctions screening & SAR filing)
- **Risk Analyst**: `risk.analyst@finxcore.com` / `FinX@2026` (Real-time fraud alerts)

---

## 4. Double-Entry Financial Ledger Invariants

Financial balances are never modified with unbacked arithmetic. Every movement writes to immutable balanced journal entries:

$$\sum \text{Debits} = \sum \text{Credits}$$

### Standard Chart of Accounts:
- `1000`: Central Bank Liquidity Reserve (ASSET)
- `1010`: Settlement Clearing Receivable (ASSET)
- `1020`: Wallet Clearing Reserve (ASSET)
- `1030`: Loans Receivable (ASSET)
- `2000`: Customer Savings Deposits (LIABILITY)
- `2010`: Customer Current Deposits (LIABILITY)
- `2020`: Customer Wallet Balances (LIABILITY)
- `2030`: Merchant Settlement Payable (LIABILITY)
- `3000`: Share Capital (EQUITY)
- `4000`: Payment Processing Fee Income (REVENUE)
- `4010`: Loan Interest Income (REVENUE)
- `5000`: Cashback & Operating Expenses (EXPENSE)

---

## 5. Running Automated Tests

Run the complete test suite:
```bash
pytest tests/
```

Test coverage includes:
1. Double-entry ledger balance invariants ($\sum \text{Debit} = \sum \text{Credit}$ and intentional rejection of unbalanced entries).
2. Transaction engine state machine transitions and concurrency locks.
3. Wallet top-up, withdrawal, and ledger escrow synchronization.
4. UPI profile registration and dynamic QR URI generation.
5. Reducing balance loan amortization calculation and credit score simulation.
6. Real-time fraud velocity rules and sanctions screening.
7. Centralized pricing MDR calculations and multi-rail automated reconciliation.
8. Comprehensive end-to-end multi-domain customer lifecycle.

---

## 6. Docker & Container Deployment

```bash
# Build and run with Docker Compose
docker-compose -f infrastructure/docker/docker-compose.yml up --build
```

---

## 7. License & Intellectual Property

FinXCore is licensed under the **FinXCore Commercial Proprietary Software License**.
Copyright (c) 2026 Dhanunjay Narra. All rights reserved.
See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE) for details.
