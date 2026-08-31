"""Reconciliation API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.reconciliation.service import reconciliation_engine

router = APIRouter(prefix="/reconciliation", tags=["Multi-Rail Reconciliation Engine"])


@router.post("/run")
def run_automated_reconciliation(db: Session = Depends(get_db)):
    return reconciliation_engine.run_reconciliation(db)
