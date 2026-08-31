"""Merchant Management API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.merchants.schemas import MerchantCreateRequest, MerchantResponse, SettlementResponse
from services.merchants.service import merchant_service
from services.merchants.models import MerchantProfile, MerchantSettlement

router = APIRouter(prefix="/merchants", tags=["Merchant Platform"])


@router.get("/profile", response_model=MerchantResponse)
def get_merchant_profile(merchant_code: str = "merch_demo_101", db: Session = Depends(get_db)):
    return merchant_service.get_or_seed_merchant(db, merchant_code)


@router.post("", response_model=MerchantResponse)
def register_merchant(req: MerchantCreateRequest, db: Session = Depends(get_db)):
    return merchant_service.create_merchant(db, req)


@router.post("/{merchant_id}/settle", response_model=SettlementResponse)
def trigger_settlement(merchant_id: str, amount: float = 125000.0, db: Session = Depends(get_db)):
    return merchant_service.trigger_settlement(db, merchant_id, amount)


@router.get("/{merchant_id}/settlements", response_model=List[SettlementResponse])
def get_settlements(merchant_id: str, db: Session = Depends(get_db)):
    settlements = db.query(MerchantSettlement).filter(MerchantSettlement.merchant_id == merchant_id).all()
    if not settlements:
        s = merchant_service.trigger_settlement(db, merchant_id, 85000.0)
        return [s]
    return settlements
