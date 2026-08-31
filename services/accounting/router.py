"""Accounting & Financial Reports API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.accounting.service import accounting_service

router = APIRouter(prefix="/accounting", tags=["Accounting & Financial Statements"])


@router.get("/statements")
def get_financial_statements(db: Session = Depends(get_db)):
    return accounting_service.get_financial_statements(db)
