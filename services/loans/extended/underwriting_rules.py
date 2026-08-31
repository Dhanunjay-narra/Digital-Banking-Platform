"""Credit Underwriting Decision Engine, Debt-to-Income & FOIR Analysis."""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from decimal import Decimal


class UnderwritingApplicant(BaseModel):
    applicant_id: str
    age: int = Field(..., ge=18, le=75)
    monthly_gross_income: float = Field(..., gt=0)
    existing_monthly_obligations: float = Field(default=0.0, ge=0)
    credit_bureau_score: int = Field(..., ge=300, le=900)
    employment_type: str = "SALARIED"  # SALARIED, SELF_EMPLOYED_PROFESSIONAL, BUSINESS
    work_experience_years: float = Field(default=2.0, ge=0)
    residence_type: str = "OWNED"  # OWNED, RENTED, PARENTAL
    collateral_value: Optional[float] = 0.0


class UnderwritingDecision(BaseModel):
    is_approved: bool
    risk_grade: str  # AAA, AA, A, BBB, BB, B, REJECT
    approved_amount: float
    approved_tenure_months: int
    interest_rate_annual: float
    monthly_emi: float
    foir_percentage: float
    max_eligible_emi: float
    rejection_reasons: List[str]
    underwriting_notes: str


class CreditUnderwritingEngine:
    """Evaluates credit applicants against comprehensive risk and financial safety policies."""

    @staticmethod
    def evaluate_loan_application(
        applicant: UnderwritingApplicant,
        requested_amount: float,
        requested_tenure_months: int,
        loan_type: str = "PERSONAL"
    ) -> UnderwritingDecision:
        rejection_reasons = []

        # 1. Age Eligibility
        if applicant.age < 21:
            rejection_reasons.append("Applicant age below minimum threshold of 21 years.")
        if applicant.age + (requested_tenure_months / 12) > 65:
            rejection_reasons.append("Loan maturity age exceeds retirement cutoff of 65 years.")

        # 2. Credit Score Eligibility
        if applicant.credit_bureau_score < 650:
            rejection_reasons.append(f"Bureau credit score {applicant.credit_bureau_score} below minimum threshold of 650.")

        # 3. Income & FOIR (Fixed Obligation to Income Ratio)
        income = applicant.monthly_gross_income
        if income < 25000.0:
            rejection_reasons.append(f"Monthly income ₹{income:.2f} below minimum threshold of ₹25,000.")

        # Allowable FOIR based on income slabs:
        # < 50k: max 45%, 50k - 100k: max 50%, > 100k: max 60%
        if income < 50000.0:
            max_foir_allowed = 0.45
        elif income <= 100000.0:
            max_foir_allowed = 0.50
        else:
            max_foir_allowed = 0.60

        max_total_emi = income * max_foir_allowed
        existing_emi = applicant.existing_monthly_obligations
        max_eligible_new_emi = max(0.0, max_total_emi - existing_emi)

        # 4. Interest Rate & Risk Grade Assignment
        if applicant.credit_bureau_score >= 800:
            risk_grade = "AAA"
            base_rate = 10.25
        elif applicant.credit_bureau_score >= 750:
            risk_grade = "AA"
            base_rate = 11.50
        elif applicant.credit_bureau_score >= 700:
            risk_grade = "A"
            base_rate = 13.00
        elif applicant.credit_bureau_score >= 650:
            risk_grade = "BBB"
            base_rate = 15.00
        else:
            risk_grade = "REJECT"
            base_rate = 18.00

        # Adjust rate by loan type
        if loan_type == "HOME":
            base_rate -= 3.0
        elif loan_type == "AUTO":
            base_rate -= 2.0

        # Calculate requested EMI using standard reducing formula
        monthly_rate = (base_rate / 100.0) / 12.0
        n = requested_tenure_months
        pow_factor = (1.0 + monthly_rate) ** n
        emi = (requested_amount * monthly_rate * pow_factor) / (pow_factor - 1.0)

        total_projected_obligations = existing_emi + emi
        projected_foir = (total_projected_obligations / income) * 100.0

        if emi > max_eligible_new_emi:
            rejection_reasons.append(
                f"Requested EMI ₹{emi:.2f} exceeds max allowable capacity ₹{max_eligible_new_emi:.2f} (Projected FOIR: {projected_foir:.1f}% > {max_foir_allowed*100:.0f}%)."
            )

        is_approved = len(rejection_reasons) == 0

        # Calculate approved amount (if rejected due to amount, offer max eligible amount)
        if not is_approved and len(rejection_reasons) == 1 and "Requested EMI" in rejection_reasons[0]:
            # Back-calculate max loan amount for max_eligible_new_emi
            max_loan = (max_eligible_new_emi * (pow_factor - 1.0)) / (monthly_rate * pow_factor)
            approved_amount = round(max_loan, -3)  # Round to nearest thousand
        elif is_approved:
            approved_amount = requested_amount
        else:
            approved_amount = 0.0

        notes = f"Risk Grade {risk_grade}. Score: {applicant.credit_bureau_score}. DTI/FOIR: {projected_foir:.1f}%."

        return UnderwritingDecision(
            is_approved=is_approved,
            risk_grade=risk_grade,
            approved_amount=approved_amount,
            approved_tenure_months=requested_tenure_months if is_approved else 0,
            interest_rate_annual=base_rate,
            monthly_emi=round(emi, 2) if is_approved else 0.0,
            foir_percentage=round(projected_foir, 1),
            max_eligible_emi=round(max_eligible_new_emi, 2),
            rejection_reasons=rejection_reasons,
            underwriting_notes=notes
        )
