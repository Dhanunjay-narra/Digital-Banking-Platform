"""Loan Management API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.loans.schemas import LoanApplyRequest, LoanRepayRequest, LoanResponse, LoanRepaymentItem
from services.loans.service import loan_service
from services.loans.models import LoanApplication, LoanRepayment

router = APIRouter(prefix="/loans", tags=["Loan Management"])


@router.post("/apply", response_model=LoanResponse)
def apply_loan(req: LoanApplyRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return loan_service.apply_for_loan(db, customer.id, req)


@router.get("", response_model=List[LoanResponse])
def get_my_loans(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    loans = db.query(LoanApplication).filter(LoanApplication.customer_id == customer.id).all()
    if not loans:
        # Seed an active personal loan for demo
        loan = loan_service.apply_for_loan(db, customer.id, LoanApplyRequest(
            loan_type="PERSONAL",
            amount=200000.0,
            tenure_months=24
        ))
        return [loan]
    return loans


@router.get("/{loan_id}/schedule", response_model=List[LoanRepaymentItem])
def get_repayment_schedule(loan_id: str, db: Session = Depends(get_db)):
    return db.query(LoanRepayment).filter(LoanRepayment.loan_id == loan_id).order_by(LoanRepayment.installment_number.asc()).all()


@router.post("/repay")
def repay_loan_installment(req: LoanRepayRequest, db: Session = Depends(get_db)):
    return loan_service.repay_installment(db, req)
