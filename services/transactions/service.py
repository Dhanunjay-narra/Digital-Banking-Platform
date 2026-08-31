"""Core Transaction Engine with State Machine & Ledger Integration."""

import json
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from finx_platform.common.exceptions import (
    FinTechException,
    InsufficientFundsException,
    AccountFrozenException,
    IdempotencyConflictException,
    EntityNotFoundException
)
from finx_platform.common.lock import lock_manager
from finx_platform.common.idempotency import idempotency_store
from finx_platform.observability.metrics import metrics
from finx_platform.observability.logger import get_logger
from services.transactions.models import FinancialTransaction, TransactionStatus, TransactionType
from services.transactions.schemas import TransactionInitiateRequest
from services.accounts.models import BankAccount
from services.ledger.service import ledger_service
from services.ledger.schemas import JournalEntryCreate, PostingCreate

logger = get_logger("transaction.engine")


class TransactionEngine:
    @staticmethod
    def execute_transaction(db: Session, req: TransactionInitiateRequest) -> FinancialTransaction:
        metrics.inc("transactions_initiated_total")

        # 1. Check Idempotency
        if req.idempotency_key:
            idempotency_store.check_or_set_processing(req.idempotency_key)
            existing_tx = db.query(FinancialTransaction).filter(FinancialTransaction.idempotency_key == req.idempotency_key).first()
            if existing_tx:
                return existing_tx

        # Generate unique transaction reference
        tx_ref = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

        tx = FinancialTransaction(
            transaction_reference=tx_ref,
            idempotency_key=req.idempotency_key,
            source_account=req.source_account,
            destination_account=req.destination_account,
            amount=req.amount,
            currency=req.currency,
            fee_amount=0.0,
            transaction_type=req.transaction_type,
            channel=req.channel,
            status=TransactionStatus.INITIATED.value,
            description=req.description,
            metadata_json=json.dumps(req.metadata) if req.metadata else None
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)

        # 2. Concurrency Lock on Source Account
        with lock_manager.acquire(req.source_account):
            try:
                # State: VALIDATING
                tx.status = TransactionStatus.VALIDATING.value
                db.commit()

                source_acc = db.query(BankAccount).filter(BankAccount.account_number == req.source_account).first()
                dest_acc = db.query(BankAccount).filter(BankAccount.account_number == req.destination_account).first()

                if source_acc:
                    if source_acc.status == "FROZEN":
                        raise AccountFrozenException(f"Source account {req.source_account} is frozen.")
                    if source_acc.available_balance < req.amount:
                        raise InsufficientFundsException(f"Account {req.source_account} has insufficient balance.")

                if dest_acc and dest_acc.status == "FROZEN":
                    raise AccountFrozenException(f"Destination account {req.destination_account} is frozen.")

                # State: AUTHORIZED
                tx.status = TransactionStatus.AUTHORIZED.value
                db.commit()

                # State: PROCESSING
                tx.status = TransactionStatus.PROCESSING.value
                db.commit()

                # Debit source account balance if in our database
                if source_acc:
                    source_acc.available_balance -= req.amount
                # Credit destination account balance if in our database
                if dest_acc:
                    dest_acc.available_balance += req.amount

                # State: POSTED (Authoritative Double-Entry Ledger)
                ledger_service.post_journal_entry(db, JournalEntryCreate(
                    transaction_id=tx.transaction_reference,
                    description=f"{req.transaction_type}: {req.description}",
                    currency=req.currency,
                    postings=[
                        PostingCreate(
                            account_code=source_acc.ledger_account_code if source_acc else "2000",
                            entry_type="DEBIT",
                            amount=req.amount,
                            description=f"Debit for {tx.transaction_reference}"
                        ),
                        PostingCreate(
                            account_code=dest_acc.ledger_account_code if dest_acc else "2010",
                            entry_type="CREDIT",
                            amount=req.amount,
                            description=f"Credit for {tx.transaction_reference}"
                        )
                    ]
                ))

                # State: COMPLETED
                tx.status = TransactionStatus.COMPLETED.value
                db.commit()
                db.refresh(tx)

                metrics.inc("transactions_successful_total")
                logger.info(f"Transaction {tx_ref} completed successfully", amount=req.amount, source=req.source_account)
                return tx

            except Exception as e:
                db.rollback()
                tx.status = TransactionStatus.FAILED.value
                tx.failure_reason = str(e)
                db.commit()
                metrics.inc("transactions_failed_total")
                logger.error(f"Transaction {tx_ref} failed: {str(e)}", source=req.source_account)
                raise e

    @staticmethod
    def reverse_transaction(db: Session, tx_id: str, reason: str) -> FinancialTransaction:
        tx = db.query(FinancialTransaction).filter(FinancialTransaction.id == tx_id).first()
        if not tx:
            raise EntityNotFoundException("Transaction", tx_id)
        if tx.status != TransactionStatus.COMPLETED.value:
            raise FinTechException("Only COMPLETED transactions can be reversed", code="INVALID_REVERSAL_STATE", status_code=400)

        # Reversal transaction
        reversal_req = TransactionInitiateRequest(
            source_account=tx.destination_account,
            destination_account=tx.source_account,
            amount=tx.amount,
            currency=tx.currency,
            transaction_type=TransactionType.REVERSAL.value,
            description=f"Reversal of {tx.transaction_reference}: {reason}"
        )
        rev_tx = TransactionEngine.execute_transaction(db, reversal_req)
        tx.status = TransactionStatus.REVERSED.value
        db.commit()
        return rev_tx


transaction_engine = TransactionEngine()
