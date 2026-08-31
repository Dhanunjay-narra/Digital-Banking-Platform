"""Digital Wallet Business Logic Service with Double-Entry Ledger."""

import random
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from finx_platform.common.exceptions import FinTechException, InsufficientFundsException, EntityNotFoundException
from services.wallet.models import DigitalWallet, WalletTransaction
from services.wallet.schemas import WalletTopupRequest, WalletWithdrawRequest, WalletTransferRequest
from services.accounts.models import BankAccount
from services.ledger.service import ledger_service
from services.ledger.schemas import JournalEntryCreate, PostingCreate


class WalletService:
    @staticmethod
    def get_or_create_wallet(db: Session, customer_id: str) -> DigitalWallet:
        wallet = db.query(DigitalWallet).filter(DigitalWallet.customer_id == customer_id).first()
        if not wallet:
            wallet_num = f"WAL{random.randint(1000000000, 9999999999)}"
            wallet = DigitalWallet(
                customer_id=customer_id,
                wallet_number=wallet_num,
                balance=15000.0,  # Demo initial balance for test ease
                currency="INR",
                status="ACTIVE",
                daily_limit=50000.0,
                monthly_limit=200000.0
            )
            db.add(wallet)
            db.commit()
            db.refresh(wallet)
        return wallet

    @staticmethod
    def top_up_wallet(db: Session, customer_id: str, req: WalletTopupRequest) -> DigitalWallet:
        wallet = WalletService.get_or_create_wallet(db, customer_id)
        source_acc = db.query(BankAccount).filter(BankAccount.account_number == req.source_bank_account).first()

        if source_acc:
            if source_acc.available_balance < req.amount:
                raise InsufficientFundsException("Insufficient funds in bank account for wallet top-up.")
            source_acc.available_balance -= req.amount

        wallet.balance += req.amount
        ref_id = f"WLT-TOP-{uuid.uuid4().hex[:8].upper()}"

        tx = WalletTransaction(
            wallet_id=wallet.id,
            transaction_type="TOP_UP",
            amount=req.amount,
            balance_after=wallet.balance,
            description=f"Top-up from Bank Account {req.source_bank_account}",
            reference_id=ref_id
        )
        db.add(tx)

        # Ledger posting: Debit Bank Deposits (2000), Credit Wallet Liability (2020)
        ledger_service.post_journal_entry(db, JournalEntryCreate(
            transaction_id=ref_id,
            description=f"Wallet Top-Up from {req.source_bank_account}",
            currency="INR",
            postings=[
                PostingCreate(account_code="2000", entry_type="DEBIT", amount=req.amount, description="Customer Account Debit"),
                PostingCreate(account_code="2020", entry_type="CREDIT", amount=req.amount, description="Wallet Escrow Credit")
            ]
        ))

        db.commit()
        db.refresh(wallet)
        return wallet

    @staticmethod
    def withdraw_to_bank(db: Session, customer_id: str, req: WalletWithdrawRequest) -> DigitalWallet:
        wallet = WalletService.get_or_create_wallet(db, customer_id)
        if wallet.balance < req.amount:
            raise InsufficientFundsException("Insufficient wallet balance for withdrawal.")

        dest_acc = db.query(BankAccount).filter(BankAccount.account_number == req.destination_bank_account).first()
        if dest_acc:
            dest_acc.available_balance += req.amount

        wallet.balance -= req.amount
        ref_id = f"WLT-WTH-{uuid.uuid4().hex[:8].upper()}"

        tx = WalletTransaction(
            wallet_id=wallet.id,
            transaction_type="WITHDRAWAL",
            amount=req.amount,
            balance_after=wallet.balance,
            description=f"Withdrawal to Bank Account {req.destination_bank_account}",
            reference_id=ref_id
        )
        db.add(tx)

        # Ledger posting: Debit Wallet Liability (2020), Credit Bank Deposits (2000)
        ledger_service.post_journal_entry(db, JournalEntryCreate(
            transaction_id=ref_id,
            description=f"Wallet Withdrawal to {req.destination_bank_account}",
            currency="INR",
            postings=[
                PostingCreate(account_code="2020", entry_type="DEBIT", amount=req.amount, description="Wallet Escrow Debit"),
                PostingCreate(account_code="2000", entry_type="CREDIT", amount=req.amount, description="Customer Account Credit")
            ]
        ))

        db.commit()
        db.refresh(wallet)
        return wallet


wallet_service = WalletService()
