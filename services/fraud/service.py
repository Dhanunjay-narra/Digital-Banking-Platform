"""Real-Time Fraud & Anomaly Detection Engine."""

import json
from datetime import datetime, timezone
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from finx_platform.observability.metrics import metrics
from finx_platform.observability.logger import get_logger
from services.fraud.models import FraudAlert, RiskDecision
from services.fraud.schemas import FraudEvaluationRequest, FraudEvaluationResponse

logger = get_logger("fraud.engine")


class FraudEngine:
    @staticmethod
    def evaluate_risk(db: Session, req: FraudEvaluationRequest) -> FraudEvaluationResponse:
        risk_score = 10.0
        triggered_rules: List[str] = []

        # Rule 1: High Transaction Amount Velocity
        if req.amount > 500000.0:
            risk_score += 45.0
            triggered_rules.append("RULE_LARGE_AMOUNT_THRESHOLD_EXCEEDED")

        # Rule 2: Suspicious IP / Unknown Device
        if req.ip_address in ["185.220.101.5", "10.0.0.99"]:
            risk_score += 35.0
            triggered_rules.append("RULE_HIGH_RISK_TOR_OR_PROXY_IP")

        # Rule 3: Mule Account or Frequent destination
        if "mule" in req.destination_account.lower() or "suspicious" in req.destination_account.lower():
            risk_score += 40.0
            triggered_rules.append("RULE_MULE_ACCOUNT_PATTERN_MATCH")

        risk_score = min(100.0, risk_score)

        if risk_score >= 70.0:
            decision = RiskDecision.BLOCK.value
        elif risk_score >= 40.0:
            decision = RiskDecision.REVIEW.value
        else:
            decision = RiskDecision.ALLOW.value

        alert_id = None
        if decision in [RiskDecision.REVIEW.value, RiskDecision.BLOCK.value]:
            metrics.inc("fraud_cases_detected_total")
            alert = FraudAlert(
                transaction_ref=req.transaction_ref,
                customer_id=req.customer_id,
                risk_score=risk_score,
                risk_decision=decision,
                triggered_rules=json.dumps(triggered_rules),
                status="OPEN"
            )
            db.add(alert)
            db.commit()
            db.refresh(alert)
            alert_id = alert.id
            logger.warning(f"Fraud alert raised for {req.transaction_ref}", score=risk_score, decision=decision)

        return FraudEvaluationResponse(
            transaction_ref=req.transaction_ref,
            risk_score=risk_score,
            risk_decision=decision,
            triggered_rules=triggered_rules,
            alert_id=alert_id
        )


fraud_engine = FraudEngine()
