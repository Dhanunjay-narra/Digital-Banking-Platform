"""Credit Scoring API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.credit.schemas import CreditScoreResponse, ScoreSimulationRequest
from services.credit.service import credit_engine

router = APIRouter(prefix="/credit", tags=["Credit Scoring Engine"])


@router.get("/score", response_model=CreditScoreResponse)
def get_my_credit_score(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return credit_engine.get_score_details(db, customer.id)


@router.post("/simulate")
def simulate_credit_score(req: ScoreSimulationRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return credit_engine.simulate_score(db, customer.id, req)
