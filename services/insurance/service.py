"""Insurance Platform Business Logic."""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, InsufficientFundsException
from services.insurance.models import InsurancePolicy, InsuranceClaim, PolicyType
from services.insurance.schemas import InsuranceQuoteRequest, PolicyBuyRequest, ClaimCreateRequest
from services.accounts.models import BankAccount


class InsuranceService:
    @staticmethod
    def calculate_quote(req: InsuranceQuoteRequest) -> Dict[str, Any]:
        # Actuarial base rate computation
        base_rate = 0.015 if req.policy_type == "HEALTH" else 0.005 if req.policy_type == "TERM_LIFE" else 0.03
        age_multiplier = 1.0 + max(0, (req.age - 25) * 0.02)
        annual_premium = round(req.sum_insured * base_rate * age_multiplier, 2)

        return {
            "policy_type": req.policy_type,
            "sum_insured": req.sum_insured,
            "annual_premium": annual_premium,
            "monthly_premium": round(annual_premium / 12, 2),
            "cashless_hospitals_count": 12500,
            "claim_settlement_ratio": "99.4%"
        }

    @staticmethod
    def buy_policy(db: Session, customer_id: str, req: PolicyBuyRequest) -> InsurancePolicy:
        # Deduct premium from bank account
        acc = db.query(BankAccount).filter(BankAccount.account_number == req.source_account_number).first()
        if acc:
            if acc.available_balance < req.annual_premium:
                raise InsufficientFundsException("Insufficient funds in account to purchase insurance policy.")
            acc.available_balance -= req.annual_premium

        now = datetime.now(timezone.utc)
        pol_num = f"POL-{datetime.now(timezone.utc).strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"

        policy = InsurancePolicy(
            policy_number=pol_num,
            customer_id=customer_id,
            policy_type=req.policy_type,
            plan_name=req.plan_name,
            sum_insured=req.sum_insured,
            annual_premium=req.annual_premium,
            status="ACTIVE",
            start_date=now,
            expiry_date=now + timedelta(days=365)
        )
        db.add(policy)
        db.commit()
        db.refresh(policy)
        return policy

    @staticmethod
    def file_claim(db: Session, req: ClaimCreateRequest) -> InsuranceClaim:
        claim_num = f"CLM-{uuid.uuid4().hex[:8].upper()}"
        claim = InsuranceClaim(
            claim_number=claim_num,
            policy_id=req.policy_id,
            claim_amount=req.claim_amount,
            reason=req.reason,
            status="SUBMITTED"
        )
        db.add(claim)
        db.commit()
        db.refresh(claim)
        return claim


insurance_service = InsuranceService()
