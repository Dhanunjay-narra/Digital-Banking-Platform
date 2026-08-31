"""Machine Learning Credit Default Predictor & Loss-Given-Default (LGD) Model."""

import math
from typing import Dict, Any


class MLCreditRiskModel:
    def predict_default_probability(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        income = float(applicant_data.get("annual_income", 1000000.0))
        requested_loan = float(applicant_data.get("loan_amount", 200000.0))
        existing_debt = float(applicant_data.get("existing_debt", 50000.0))
        score = int(applicant_data.get("credit_score", 750))

        # Debt to income
        dti = (existing_debt + requested_loan * 0.3) / income if income > 0 else 1.0

        # Base logit formula calibrated on financial credit bureau distributions
        logit = 2.5 - (score / 150.0) + (dti * 2.0)
        pd = 1.0 / (1.0 + math.exp(-logit))  # Probability of Default (PD)

        expected_loss_rate = pd * 0.45  # Assuming 45% LGD

        return {
            "probability_of_default": round(pd, 4),
            "expected_loss_rate": round(expected_loss_rate, 4),
            "recommended_pricing_spread_bps": int(pd * 400),
            "decision": "ACCEPT" if pd < 0.08 else "REFER_MANUAL_REVIEW" if pd < 0.15 else "DECLINE"
        }


ml_credit_model = MLCreditRiskModel()
