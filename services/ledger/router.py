"""Double-Entry Financial Ledger API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.ledger.schemas import (
    JournalEntryCreate,
    LedgerAccountCreate,
    LedgerAccountResponse,
    TrialBalanceResponse
)
from services.ledger.service import ledger_service
from services.ledger.models import LedgerAccount, JournalEntry

router = APIRouter(prefix="/ledger", tags=["Double-Entry Financial Ledger"])


@router.get("/accounts", response_model=List[LedgerAccountResponse])
def list_ledger_accounts(db: Session = Depends(get_db)):
    ledger_service.initialize_chart_of_accounts(db)
    return db.query(LedgerAccount).all()


@router.post("/accounts", response_model=LedgerAccountResponse)
def create_ledger_account(req: LedgerAccountCreate, db: Session = Depends(get_db)):
    return ledger_service.get_or_create_account(db, req)


@router.post("/journal-entries")
def post_journal_entry(req: JournalEntryCreate, db: Session = Depends(get_db)):
    entry = ledger_service.post_journal_entry(db, req)
    return {
        "success": True,
        "entry_id": entry.id,
        "entry_number": entry.entry_number,
        "total_debit": entry.total_debit,
        "total_credit": entry.total_credit,
        "status": entry.status
    }


@router.get("/journal-entries")
def list_journal_entries(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(JournalEntry).order_by(JournalEntry.created_at.desc()).limit(limit).all()


@router.get("/trial-balance", response_model=TrialBalanceResponse)
def get_trial_balance(db: Session = Depends(get_db)):
    ledger_service.initialize_chart_of_accounts(db)
    return ledger_service.get_trial_balance(db)
