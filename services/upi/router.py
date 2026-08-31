"""UPI Rail Simulator API Endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.upi.schemas import (
    VPARegisterRequest,
    UPISendRequest,
    UPICollectCreateRequest,
    QRCodeGenerateRequest,
    UPIProfileResponse,
    UPITransactionResponse
)
from services.upi.service import upi_service
from services.upi.models import UPIProfile, UPICollectRequest

router = APIRouter(prefix="/upi", tags=["UPI-Like Instant Rail Simulator"])


@router.get("/profile", response_model=UPIProfileResponse)
def get_upi_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return upi_service.get_or_create_profile(db, customer.id)


@router.post("/send", response_model=UPITransactionResponse)
def send_upi_payment(req: UPISendRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return upi_service.send_money(db, customer.id, req)


@router.post("/qr/generate")
def generate_upi_qr(req: QRCodeGenerateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return upi_service.generate_qr(db, customer.id, req)


@router.post("/collect")
def create_collect_request(req: UPICollectCreateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return upi_service.create_collect_request(db, customer.id, req)


@router.get("/collect/requests")
def get_collect_requests(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    profile = upi_service.get_or_create_profile(db, customer.id)
    return db.query(UPICollectRequest).filter(
        (UPICollectRequest.requester_vpa == profile.vpa_address) | (UPICollectRequest.payer_vpa == profile.vpa_address)
    ).all()
