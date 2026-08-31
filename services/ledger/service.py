"""Authoritative Double-Entry Financial Ledger Service."""

import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from finx_platform.common.exceptions import UnbalancedLedgerException, EntityNotFoundException, FinTechException
from finx_platform.common.math_utils import to_decimal
from services.ledger.models import LedgerAccount, JournalEntry, LedgerPosting, AccountType, EntryType
from services.ledger.schemas import JournalEntryCreate, LedgerAccountCreate, TrialBalanceResponse, TrialBalanceItem


class LedgerService:
    @staticmethod
    def initialize_chart_of_accounts(db: Session) -> None:
        """Seed standard financial chart of accounts."""
        defaults = [
            # ASSETS
            ("1000", "Central Bank Vault / Cash Reserve", AccountType.ASSET, "Bank primary liquidity reserve"),
            ("1010", "Settlement Clearing Account", AccountType.ASSET, "Interbank settlement receivable"),
            ("1020", "Wallet Clearing Reserve", AccountType.ASSET, "Escrow pool backing customer wallets"),
            ("1030", "Loans Receivable", AccountType.ASSET, "Principal outstanding from active loans"),
            # LIABILITIES
            ("2000", "Customer Savings Deposits", AccountType.LIABILITY, "Total customer savings liability"),
            ("2010", "Customer Current Deposits", AccountType.LIABILITY, "Total customer current deposits"),
            ("2020", "Customer Wallet Balances", AccountType.LIABILITY, "Prepaid wallet balances liability"),
            ("2030", "Merchant Settlement Payable", AccountType.LIABILITY, "Unsettled funds owed to merchants"),
            ("2090", "Suspense Account", AccountType.LIABILITY, "Unallocated funds awaiting reconciliation"),
            # EQUITY
            ("3000", "Share Capital", AccountType.EQUITY, "Initial core tier-1 banking capital"),
            ("3010", "Retained Earnings", AccountType.EQUITY, "Accumulated platform operating profit"),
            # REVENUE
            ("4000", "Payment Processing Fee Income", AccountType.REVENUE, "MDR and payment gateway transaction fees"),
            ("4010", "Loan Interest Income", AccountType.REVENUE, "Interest collected from loan repayments"),
            ("4020", "Card Interchange & Annual Fees", AccountType.REVENUE, "Fee income from card platform"),
            # EXPENSES
            ("5000", "Cashback & Reward Expense", AccountType.EXPENSE, "Reward points and cashback distributions"),
            ("5010", "Network Interchange Expense", AccountType.EXPENSE, "NPCI / VISA network switching fees"),
            ("5020", "Operating Expense", AccountType.EXPENSE, "Infrastructure and cloud operating cost"),
        ]

        for code, name, acc_type, desc in defaults:
            existing = db.query(LedgerAccount).filter(LedgerAccount.account_code == code).first()
            if not existing:
                acc = LedgerAccount(
                    account_code=code,
                    account_name=name,
                    account_type=acc_type.value,
                    currency="INR",
                    balance=100000000.0 if code == "1000" or code == "3000" else 0.0,
                    description=desc
                )
                db.add(acc)
        db.commit()

    @staticmethod
    def get_or_create_account(db: Session, req: LedgerAccountCreate) -> LedgerAccount:
        acc = db.query(LedgerAccount).filter(LedgerAccount.account_code == req.account_code).first()
        if not acc:
            acc = LedgerAccount(
                account_code=req.account_code,
                account_name=req.account_name,
                account_type=req.account_type,
                currency=req.currency,
                balance=0.0,
                description=req.description
            )
            db.add(acc)
            db.commit()
            db.refresh(acc)
        return acc

    @staticmethod
    def post_journal_entry(db: Session, entry_req: JournalEntryCreate) -> JournalEntry:
        """Enforces double-entry balance: sum(DEBIT) == sum(CREDIT)"""
        if not entry_req.postings or len(entry_req.postings) < 2:
            raise UnbalancedLedgerException("A double-entry journal transaction requires at least 2 postings.")

        total_debit = 0.0
        total_credit = 0.0

        for p in entry_req.postings:
            amt = float(to_decimal(p.amount))
            if p.entry_type == "DEBIT":
                total_debit += amt
            elif p.entry_type == "CREDIT":
                total_credit += amt

        # Balance check with floating point tolerance
        if abs(total_debit - total_credit) > 0.001:
            raise UnbalancedLedgerException(
                f"Ledger entry is unbalanced! Total Debits: ₹{total_debit:.2f} != Total Credits: ₹{total_credit:.2f}",
                details={"total_debit": total_debit, "total_credit": total_credit}
            )

        journal = JournalEntry(
            entry_number=f"JRN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}",
            transaction_id=entry_req.transaction_id,
            description=entry_req.description,
            currency=entry_req.currency,
            total_debit=round(total_debit, 2),
            total_credit=round(total_credit, 2),
            status="POSTED"
        )
        db.add(journal)
        db.flush()

        for p in entry_req.postings:
            acc = db.query(LedgerAccount).filter(LedgerAccount.account_code == p.account_code).first()
            if not acc:
                acc = LedgerAccount(
                    account_code=p.account_code,
                    account_name=f"Ledger Account {p.account_code}",
                    account_type=AccountType.LIABILITY.value if p.account_code.startswith("2") else AccountType.ASSET.value,
                    currency=entry_req.currency,
                    balance=0.0
                )
                db.add(acc)
                db.flush()

            amt = float(to_decimal(p.amount))
            posting = LedgerPosting(
                journal_entry_id=journal.id,
                ledger_account_id=acc.id,
                entry_type=p.entry_type,
                amount=amt,
                description=p.description or entry_req.description
            )
            db.add(posting)

            # Update account balance based on normal balance rules:
            # Assets & Expenses increase with DEBIT, decrease with CREDIT
            # Liabilities, Equity & Revenues increase with CREDIT, decrease with DEBIT
            if acc.account_type in [AccountType.ASSET.value, AccountType.EXPENSE.value]:
                if p.entry_type == "DEBIT":
                    acc.balance += amt
                else:
                    acc.balance -= amt
            else:
                if p.entry_type == "CREDIT":
                    acc.balance += amt
                else:
                    acc.balance -= amt

        db.commit()
        db.refresh(journal)
        return journal

    @staticmethod
    def get_trial_balance(db: Session) -> TrialBalanceResponse:
        accounts = db.query(LedgerAccount).all()
        items = []
        tot_deb = 0.0
        tot_cred = 0.0

        for a in accounts:
            bal = a.balance
            if a.account_type in [AccountType.ASSET.value, AccountType.EXPENSE.value]:
                deb = bal if bal >= 0 else 0.0
                cred = abs(bal) if bal < 0 else 0.0
            else:
                cred = bal if bal >= 0 else 0.0
                deb = abs(bal) if bal < 0 else 0.0

            tot_deb += deb
            tot_cred += cred

            items.append(TrialBalanceItem(
                account_code=a.account_code,
                account_name=a.account_name,
                account_type=a.account_type,
                debit_balance=round(deb, 2),
                credit_balance=round(cred, 2)
            ))

        return TrialBalanceResponse(
            items=items,
            total_debits=round(tot_deb, 2),
            total_credits=round(tot_cred, 2),
            is_balanced=abs(tot_deb - tot_cred) < 0.01,
            generated_at=datetime.now(timezone.utc)
        )


ledger_service = LedgerService()
