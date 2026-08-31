"""AML & Sanctions Screening Service."""

import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from services.compliance.models import SanctionEntry, SARReport
from services.compliance.schemas import SanctionsCheckRequest, SanctionMatchResponse, SARCreateRequest


class ComplianceService:
    KNOWN_SANCTIONS = [
        "VIKTOR BOUT", "DAWOOD IBRAHIM", "HAFEEZ SAEED", "GUCCIFER 2.0", "LAZARUS GROUP"
    ]

    @staticmethod
    def screen_individual(db: Session, req: SanctionsCheckRequest) -> SanctionMatchResponse:
        name_clean = req.full_name.upper().strip()
        matched = False
        match_name = None

        for s in ComplianceService.KNOWN_SANCTIONS:
            if s in name_clean or name_clean in s:
                matched = True
                match_name = s
                break

        if matched:
            return SanctionMatchResponse(
                is_matched=True,
                confidence_score=95.0,
                matched_entity=match_name,
                list_source="OFAC_UN_CONSOLIDATED_WATCHLIST",
                action_required="BLOCK_AND_REPORT"
            )

        return SanctionMatchResponse(
            is_matched=False,
            confidence_score=0.0,
            matched_entity=None,
            list_source="GLOBAL_SANCTIONS_DB",
            action_required="ALLOW"
        )

    @staticmethod
    def file_sar(db: Session, req: SARCreateRequest, officer_name: str = "Compliance Officer") -> SARReport:
        sar_ref = f"SAR-{datetime.now(timezone.utc).strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
        sar = SARReport(
            sar_reference=sar_ref,
            customer_id=req.customer_id,
            suspicion_reason=req.suspicion_reason,
            narrative=req.narrative,
            involved_amount=req.involved_amount,
            status="SUBMITTED_TO_FIU",
            filed_by=officer_name
        )
        db.add(sar)
        db.commit()
        db.refresh(sar)
        return sar


compliance_service = ComplianceService()
