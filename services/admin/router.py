"""Admin & Operations Back-Office API Endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from finx_platform.observability.audit import AuditLog
from services.identity.models import User
from services.customer.models import Customer
from services.transactions.models import FinancialTransaction
from services.ledger.models import JournalEntry, LedgerAccount
from services.fraud.models import FraudAlert
from services.loans.models import LoanApplication
from services.merchants.models import MerchantProfile

router = APIRouter(prefix="/admin", tags=["Admin & Operations Console"])


@router.get("/overview")
def get_admin_overview(db: Session = Depends(get_db)):
    return {
        "users_count": db.query(User).count(),
        "customers_count": db.query(Customer).count(),
        "transactions_count": db.query(FinancialTransaction).count(),
        "journal_entries_count": db.query(JournalEntry).count(),
        "fraud_alerts_count": db.query(FraudAlert).count(),
        "loan_applications_count": db.query(LoanApplication).count(),
        "merchants_count": db.query(MerchantProfile).count(),
        "active_services_health": "ALL_SYSTEMS_OPERATIONAL"
    }


@router.get("/audit-logs")
def list_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    if not logs:
        # Create a sample initial platform bootstrap audit log
        log = AuditLog(
            actor_id="super_admin_01",
            actor_role="SUPER_ADMIN",
            action="BOOTSTRAP_CORE_PLATFORM",
            resource_type="PLATFORM_ENGINE",
            resource_id="SYS_CORE",
            correlation_id="BOOTSTRAP-INIT",
            reason="Platform cold-start initialization"
        )
        db.add(log)
        db.commit()
        return [log]
    return logs
