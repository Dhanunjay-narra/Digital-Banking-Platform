"""Investment & Wealth API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.investments.schemas import InvestmentOrderRequest, SIPCreateRequest, PortfolioSummaryResponse, HoldingResponse
from services.investments.service import investment_service
from services.investments.models import SIPPlan

router = APIRouter(prefix="/investments", tags=["Investment Platform"])


@router.get("/portfolio", response_model=PortfolioSummaryResponse)
def get_portfolio(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return investment_service.get_portfolio_summary(db, customer.id)


@router.post("/buy", response_model=HoldingResponse)
def buy_asset(req: InvestmentOrderRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return investment_service.buy_asset(db, customer.id, req)


@router.post("/sip")
def create_sip(req: SIPCreateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    plan = SIPPlan(
        customer_id=customer.id,
        asset_symbol=req.asset_symbol,
        asset_name=req.asset_name,
        monthly_amount=req.monthly_amount,
        sip_day=req.sip_day
    )
    db.add(plan)
    db.commit()
    return {"success": True, "message": "SIP created successfully", "plan_id": plan.id}
