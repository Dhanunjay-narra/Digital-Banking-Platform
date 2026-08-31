"""Financial Recommendations API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.recommendations.service import recommendation_engine

router = APIRouter(prefix="/recommendations", tags=["Financial Intelligence & AI Insights"])


@router.get("")
def get_recommendations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return recommendation_engine.generate_recommendations(db, customer.id)
