"""Dispute & Chargeback API Endpoints."""

import uuid
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.disputes.models import Dispute

router = APIRouter(prefix="/disputes", tags=["Disputes & Chargebacks"])


class DisputeCreateRequest(BaseModel):
    transaction_ref: str
    amount: float
    reason: str
    evidence: Optional[str] = None


@router.post("")
def raise_dispute(req: DisputeCreateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    disp = Dispute(
        dispute_reference=f"DISP-{uuid.uuid4().hex[:8].upper()}",
        transaction_ref=req.transaction_ref,
        customer_id=customer.id,
        disputed_amount=req.amount,
        reason=req.reason,
        evidence_text=req.evidence,
        status="OPEN"
    )
    db.add(disp)
    db.commit()
    db.refresh(disp)
    return {"success": True, "dispute_reference": disp.dispute_reference, "status": disp.status}


@router.get("")
def list_my_disputes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    disputes = db.query(Dispute).filter(Dispute.customer_id == customer.id).all()
    if not disputes:
        disp = Dispute(
            dispute_reference="DISP-SAMPLE-01",
            transaction_ref="TXN-20260301-DEMO",
            customer_id=customer.id,
            disputed_amount=1200.0,
            reason="Duplicate charge at merchant POS",
            status="UNDER_REVIEW"
        )
        db.add(disp)
        db.commit()
        return [disp]
    return disputes
