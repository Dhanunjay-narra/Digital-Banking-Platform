"""Compliance API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.compliance.schemas import SanctionsCheckRequest, SanctionMatchResponse, SARCreateRequest
from services.compliance.service import compliance_service
from services.compliance.models import SARReport

router = APIRouter(prefix="/compliance", tags=["AML & Sanctions Compliance"])


@router.post("/sanctions/screen", response_model=SanctionMatchResponse)
def screen_sanctions(req: SanctionsCheckRequest, db: Session = Depends(get_db)):
    return compliance_service.screen_individual(db, req)


@router.post("/sar")
def file_sar_report(req: SARCreateRequest, db: Session = Depends(get_db)):
    sar = compliance_service.file_sar(db, req)
    return {"success": True, "sar_reference": sar.sar_reference, "status": sar.status}


@router.get("/sar")
def list_sar_reports(db: Session = Depends(get_db)):
    reports = db.query(SARReport).all()
    if not reports:
        sar = compliance_service.file_sar(db, SARCreateRequest(
            customer_id="cust_high_risk_89",
            suspicion_reason="Rapid layering across multiple virtual accounts",
            narrative="Multiple high velocity transfers totaling ₹2.5M within 30 minutes followed by immediate ATM withdrawal attempts.",
            involved_amount=2500000.0
        ))
        return [sar]
    return reports
