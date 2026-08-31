"""Analytics API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.analytics.service import analytics_engine

router = APIRouter(prefix="/analytics", tags=["Real-Time Analytics"])


@router.get("/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    return analytics_engine.get_realtime_dashboard_metrics(db)
