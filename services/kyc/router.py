"""KYC Verification API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.kyc.schemas import KYCSubmitRequest, PANVerifyRequest, BankVerifyRequest, KYCResponse
from services.kyc.service import kyc_service
from services.kyc.models import KYCApplication

router = APIRouter(prefix="/kyc", tags=["KYC & Customer Verification"])


@router.post("/submit", response_model=KYCResponse)
def submit_kyc(req: KYCSubmitRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return kyc_service.submit_kyc(db, customer.id, req)


@router.get("/status")
def get_kyc_status(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    kyc = db.query(KYCApplication).filter(KYCApplication.customer_id == customer.id).first()
    if not kyc:
        return {"status": "NOT_INITIATED", "kyc_level": "NONE", "pan_verified": False, "bank_verified": False}
    return kyc


@router.post("/verify/pan")
def verify_pan(req: PANVerifyRequest, db: Session = Depends(get_db)):
    return kyc_service.verify_pan(db, req)


@router.post("/verify/bank")
def verify_bank(req: BankVerifyRequest, db: Session = Depends(get_db)):
    return kyc_service.verify_bank_account(db, req)
