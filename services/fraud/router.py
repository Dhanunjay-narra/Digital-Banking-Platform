"""Fraud Risk API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.fraud.schemas import FraudEvaluationRequest, FraudEvaluationResponse, FraudAlertResponse
from services.fraud.service import fraud_engine
from services.fraud.models import FraudAlert

router = APIRouter(prefix="/fraud", tags=["Fraud & Risk Engine"])


@router.post("/evaluate", response_model=FraudEvaluationResponse)
def evaluate_transaction_risk(req: FraudEvaluationRequest, db: Session = Depends(get_db)):
    return fraud_engine.evaluate_risk(db, req)


@router.get("/alerts", response_model=List[FraudAlertResponse])
def list_fraud_alerts(db: Session = Depends(get_db)):
    alerts = db.query(FraudAlert).order_by(FraudAlert.created_at.desc()).limit(50).all()
    if not alerts:
        # Seed a sample fraud alert for risk analyst dashboard
        res = fraud_engine.evaluate_risk(db, FraudEvaluationRequest(
            customer_id="cust_demo_101",
            transaction_ref="TXN-20260301-HIGH-ANOMALY",
            amount=750000.0,
            channel="WEB",
            ip_address="185.220.101.5",
            destination_account="mule_ac_99817"
        ))
        alerts = db.query(FraudAlert).all()
    return alerts


@router.post("/alerts/{alert_id}/resolve")
def resolve_fraud_alert(alert_id: str, status: str = "RESOLVED_FALSE_POSITIVE", notes: str = "Verified with customer via 2FA", db: Session = Depends(get_db)):
    alert = db.query(FraudAlert).filter(FraudAlert.id == alert_id).first()
    if alert:
        alert.status = status
        alert.resolution_notes = notes
        db.commit()
    return {"success": True, "message": "Alert updated successfully"}
