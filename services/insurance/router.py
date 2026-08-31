"""Insurance API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.insurance.schemas import (
    InsuranceQuoteRequest,
    PolicyBuyRequest,
    ClaimCreateRequest,
    InsurancePolicyResponse
)
from services.insurance.service import insurance_service
from services.insurance.models import InsurancePolicy, InsuranceClaim

router = APIRouter(prefix="/insurance", tags=["Insurance Platform"])


@router.post("/quote")
def get_quote(req: InsuranceQuoteRequest):
    return insurance_service.calculate_quote(req)


@router.post("/buy", response_model=InsurancePolicyResponse)
def buy_insurance_policy(req: PolicyBuyRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return insurance_service.buy_policy(db, customer.id, req)


@router.get("/policies", response_model=List[InsurancePolicyResponse])
def get_my_policies(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    policies = db.query(InsurancePolicy).filter(InsurancePolicy.customer_id == customer.id).all()
    if not policies:
        # Create a sample health policy for testing
        pol = insurance_service.buy_policy(db, customer.id, PolicyBuyRequest(
            policy_type="HEALTH",
            plan_name="FinX Complete Health Shield 360",
            sum_insured=1000000.0,
            annual_premium=14500.0
        ))
        return [pol]
    return policies


@router.post("/claims")
def submit_claim(req: ClaimCreateRequest, db: Session = Depends(get_db)):
    claim = insurance_service.file_claim(db, req)
    return {"success": True, "claim_number": claim.claim_number, "status": claim.status}
