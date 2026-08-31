"""Bank Transfers Service with Core Transaction Engine Routing."""

import random
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from finx_platform.common.exceptions import FinTechException, InsufficientFundsException
from services.transfers.models import BankTransfer, TransferRail
from services.transfers.schemas import TransferInitiateRequest
from services.transactions.service import transaction_engine
from services.transactions.schemas import TransactionInitiateRequest


class TransferService:
    @staticmethod
    def execute_transfer(db: Session, req: TransferInitiateRequest) -> BankTransfer:
        ref = f"TRF-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
        utr = f"FINX{datetime.now(timezone.utc).strftime('%Y%m%d')}{random.randint(1000000, 9999999)}"

        # Route through core transaction state machine
        tx = transaction_engine.execute_transaction(db, TransactionInitiateRequest(
            source_account=req.source_account,
            destination_account=req.destination_account,
            amount=req.amount,
            currency=req.currency,
            transaction_type=f"{req.rail}_TRANSFER",
            channel="WEB",
            description=f"Transfer to {req.beneficiary_name}: {req.remarks}",
            idempotency_key=req.idempotency_key,
            metadata={"rail": req.rail, "utr": utr, "beneficiary_name": req.beneficiary_name}
        ))

        transfer = BankTransfer(
            transfer_reference=ref,
            source_account=req.source_account,
            destination_account=req.destination_account,
            beneficiary_name=req.beneficiary_name,
            destination_ifsc=req.destination_ifsc,
            rail=req.rail,
            amount=req.amount,
            fee_amount=0.0,
            currency=req.currency,
            status="COMPLETED" if tx.status == "COMPLETED" else "FAILED",
            remarks=req.remarks,
            utr_number=utr
        )
        db.add(transfer)
        db.commit()
        db.refresh(transfer)
        return transfer


transfer_service = TransferService()
