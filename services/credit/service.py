"""Credit Scoring & Underwriting Engine."""

from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy.orm import Session
from platform.common.exceptions import EntityNotFoundException
from services.credit.models import CreditProfile
from services.credit.schemas import CreditScoreResponse, ScoreSimulationRequest


class CreditEngine:
    @staticmethod
    def get_or_calculate_profile(db: Session, customer_id: str) -> CreditProfile:
        profile = db.query(CreditProfile).filter(CreditProfile.customer_id == customer_id).first()
        if not profile:
            profile = CreditProfile(
                customer_id=customer_id,
                score=782,
                credit_grade="EXCELLENT",
                on_time_payment_pct=99.2,
                credit_utilization_pct=14.5,
                total_active_accounts=5,
                credit_history_years=5.2,
                recent_hard_inquiries=0,
                recommended_credit_limit=500000.0,
                last_pulled_at=datetime.now(timezone.utc)
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile

    @staticmethod
    def get_score_details(db: Session, customer_id: str) -> CreditScoreResponse:
        p = CreditEngine.get_or_calculate_profile(db, customer_id)
        factors = {
            "Payment History (35%)": "Excellent (99.2% on-time)",
            "Credit Utilization (30%)": "Optimal (< 15%)",
            "Age of Credit (15%)": "Good (5+ years)",
            "Credit Mix (10%)": "Diverse (Loans + Cards)",
            "Recent Inquiries (10%)": "Very Low (0 inquiries)"
        }
        return CreditScoreResponse(
            customer_id=p.customer_id,
            score=p.score,
            credit_grade=p.credit_grade,
            on_time_payment_pct=p.on_time_payment_pct,
            credit_utilization_pct=p.credit_utilization_pct,
            total_active_accounts=p.total_active_accounts,
            credit_history_years=p.credit_history_years,
            recent_hard_inquiries=p.recent_hard_inquiries,
            recommended_credit_limit=p.recommended_credit_limit,
            factors=factors
        )

    @staticmethod
    def simulate_score(db: Session, customer_id: str, req: ScoreSimulationRequest) -> Dict[str, Any]:
        p = CreditEngine.get_or_calculate_profile(db, customer_id)
        simulated_score = p.score

        if req.repay_all_credit_cards:
            simulated_score = min(900, simulated_score + 35)
        if req.new_loan_amount and req.new_loan_amount > 500000:
            simulated_score = max(300, simulated_score - 15)
        if req.miss_one_payment:
            simulated_score = max(300, simulated_score - 80)

        return {
            "current_score": p.score,
            "simulated_score": simulated_score,
            "score_delta": simulated_score - p.score,
            "projected_grade": "EXCELLENT" if simulated_score >= 750 else "GOOD" if simulated_score >= 680 else "FAIR"
        }


credit_engine = CreditEngine()
