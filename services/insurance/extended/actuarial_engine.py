"""Actuarial Pricing Models, Mortality Rates & Claim Adjudication Engine."""

from typing import Dict, Any, List
from datetime import datetime, timezone
import math


class ActuarialEngine:
    """Computes pure risk premiums based on standard mortality and morbidity tables."""

    MORTALITY_TABLE_PER_1000 = {
        20: 0.85, 25: 0.98, 30: 1.15, 35: 1.45, 40: 2.10,
        45: 3.25, 50: 5.40, 55: 8.90, 60: 14.50, 65: 23.80
    }

    @staticmethod
    def calculate_term_life_premium(sum_assured: float, age: int, is_smoker: bool = False, tenure_years: int = 30) -> Dict[str, Any]:
        # Interpolate mortality rate
        nearest_age = min(ActuarialEngine.MORTALITY_TABLE_PER_1000.keys(), key=lambda k: abs(k - age))
        base_mortality = ActuarialEngine.MORTALITY_TABLE_PER_1000[nearest_age] / 1000.0

        if is_smoker:
            base_mortality *= 1.65

        # Pure risk premium
        pure_risk = sum_assured * base_mortality
        loading_expense = pure_risk * 0.20  # 20% acquisition and admin loading
        profit_margin = pure_risk * 0.10    # 10% safety and profit margin
        annual_premium = pure_risk + loading_expense + profit_margin
        gst = annual_premium * 0.18

        return {
            "sum_assured": sum_assured,
            "age": age,
            "is_smoker": is_smoker,
            "annual_premium_base": round(annual_premium, 2),
            "gst_18_pct": round(gst, 2),
            "total_annual_premium": round(annual_premium + gst, 2),
            "monthly_installment": round((annual_premium + gst) / 12.0, 2)
        }

    @staticmethod
    def adjudicate_health_claim(
        claimed_amount: float,
        sum_insured_available: float,
        copay_percentage: float = 0.0,
        deductible: float = 0.0,
        is_network_hospital: bool = True
    ) -> Dict[str, Any]:
        """Automated claim adjudication rules engine."""
        effective_claim = max(0.0, claimed_amount - deductible)
        copay_deduction = effective_claim * (copay_percentage / 100.0)
        adjudicated_amount = max(0.0, effective_claim - copay_deduction)

        # Cap by available sum insured
        payable_amount = min(adjudicated_amount, sum_insured_available)
        patient_share = claimed_amount - payable_amount

        return {
            "claimed_amount": claimed_amount,
            "deductible_applied": deductible,
            "copay_deducted": round(copay_deduction, 2),
            "approved_payable_amount": round(payable_amount, 2),
            "patient_out_of_pocket": round(patient_share, 2),
            "claim_status": "APPROVED" if payable_amount > 0 else "REJECTED_EXCEEDS_LIMITS",
            "settlement_channel": "CASHLESS_TPA_SETTLEMENT" if is_network_hospital else "REIMBURSEMENT_DIRECT"
        }
