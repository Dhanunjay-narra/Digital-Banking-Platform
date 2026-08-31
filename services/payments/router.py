"""Merchant Payment Gateway API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.payments.schemas import (
    PaymentOrderCreate,
    PaymentCaptureRequest,
    PaymentRefundRequest,
    PaymentOrderResponse
)
from services.payments.service import payment_gateway_service
from services.payments.models import PaymentOrder

router = APIRouter(prefix="/payments", tags=["Payment Gateway"])


@router.post("/orders", response_model=PaymentOrderResponse)
def create_payment_order(req: PaymentOrderCreate, db: Session = Depends(get_db)):
    return payment_gateway_service.create_order(db, req)


@router.post("/capture", response_model=PaymentOrderResponse)
def capture_payment(req: PaymentCaptureRequest, db: Session = Depends(get_db)):
    return payment_gateway_service.capture_payment(db, req)


@router.post("/refund")
def refund_payment(req: PaymentRefundRequest, db: Session = Depends(get_db)):
    return payment_gateway_service.refund_payment(db, req)


@router.get("/orders", response_model=List[PaymentOrderResponse])
def list_orders(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(PaymentOrder).order_by(PaymentOrder.created_at.desc()).limit(limit).all()
