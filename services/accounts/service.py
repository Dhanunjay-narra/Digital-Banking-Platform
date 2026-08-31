"""Banking Accounts Service with Ledger Integration."""

import random
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, AccountFrozenException, InsufficientFundsException, EntityNotFoundException
from services.accounts.models import BankAccount, AccountHold
from services.accounts.schemas import AccountCreateRequest
from services.ledger.service import ledger_service
from services.ledger.schemas import JournalEntryCreate, PostingCreate


class AccountService:
    @staticmethod
    def generate_account_number(account_type: str) -> str:
        prefix = "1000" if account_type == "SAVINGS" else "2000" if account_type == "CURRENT" else "3000"
        return f"{prefix}{random.randint(10000000, 99999999)}"

    @staticmethod
    def open_account(db: Session, customer_id: str, req: AccountCreateRequest) -> BankAccount:
        ledger_service.initialize_chart_of_accounts(db)

        acc_num = AccountService.generate_account_number(req.account_type)
        ledger_code = f"2000.{acc_num[-6:]}" if req.account_type == "SAVINGS" else f"2010.{acc_num[-6:]}"

        account = BankAccount(
            customer_id=customer_id,
            account_number=acc_num,
            account_type=req.account_type,
            currency=req.currency,
            status="ACTIVE",
            ledger_account_code=ledger_code,
            available_balance=req.initial_deposit,
            hold_balance=0.0,
            minimum_balance=1000.0 if req.account_type == "SAVINGS" else 10000.0,
            interest_rate_percent=4.0 if req.account_type == "SAVINGS" else 0.0,
            branch_ifsc="FINX0001001"
        )
        db.add(account)
        db.commit()
        db.refresh(account)

        # If initial deposit > 0, post authoritative double-entry journal entry:
        # Debit Cash Reserve (1000), Credit Customer Deposits (2000/2010)
        if req.initial_deposit > 0:
            ledger_service.post_journal_entry(db, JournalEntryCreate(
                transaction_id=f"OPEN-{account.account_number}",
                description=f"Initial deposit for new {req.account_type} Account {acc_num}",
                currency=req.currency,
                postings=[
                    PostingCreate(account_code="1000", entry_type="DEBIT", amount=req.initial_deposit, description="Cash Reserve inflow"),
                    PostingCreate(account_code="2000" if req.account_type == "SAVINGS" else "2010", entry_type="CREDIT", amount=req.initial_deposit, description=f"Deposit credit to {acc_num}")
                ]
            ))

        return account

    @staticmethod
    def freeze_account(db: Session, account_number: str, reason: str) -> BankAccount:
        acc = db.query(BankAccount).filter(BankAccount.account_number == account_number).first()
        if not acc:
            raise EntityNotFoundException("BankAccount", account_number)
        acc.status = "FROZEN"
        db.commit()
        db.refresh(acc)
        return acc

    @staticmethod
    def unfreeze_account(db: Session, account_number: str) -> BankAccount:
        acc = db.query(BankAccount).filter(BankAccount.account_number == account_number).first()
        if not acc:
            raise EntityNotFoundException("BankAccount", account_number)
        acc.status = "ACTIVE"
        db.commit()
        db.refresh(acc)
        return acc


account_service = AccountService()
