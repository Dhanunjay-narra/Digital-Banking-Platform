"""Transaction API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.transactions.schemas import TransactionInitiateRequest, TransactionResponse
from services.transactions.service import transaction_engine
from services.transactions.models import FinancialTransaction

router = APIRouter(prefix="/transactions", tags=["Core Transaction Engine"])


@router.post("", response_model=TransactionResponse)
def initiate_transaction(req: TransactionInitiateRequest, db: Session = Depends(get_db)):
    return transaction_engine.execute_transaction(db, req)


@router.get("", response_model=List[TransactionResponse])
def get_transaction_history(
    account_number: str = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(FinancialTransaction)
    if account_number:
        query = query.filter((FinancialTransaction.source_account == account_number) | (FinancialTransaction.destination_account == account_number))
    return query.order_by(FinancialTransaction.created_at.desc()).limit(limit).all()


@router.post("/{tx_id}/reverse", response_model=TransactionResponse)
def reverse_transaction(tx_id: str, reason: str = Query("Customer dispute resolution"), db: Session = Depends(get_db)):
    return transaction_engine.reverse_transaction(db, tx_id, reason)
