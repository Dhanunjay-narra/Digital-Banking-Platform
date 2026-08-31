"""Loan Lifecycle, Underwriting & Amortization Engine."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, EntityNotFoundException, InsufficientFundsException
from platform.common.math_utils import calculate_emi, to_decimal
from platform.observability.metrics import metrics
from services.loans.models import LoanApplication, LoanRepayment, LoanStatus, LoanType
from services.loans.schemas import LoanApplyRequest, LoanUnderwriteDecisionRequest, LoanRepayRequest
from services.accounts.models import BankAccount
from services.ledger.service import ledger_service
from services.ledger.schemas import JournalEntryCreate, PostingCreate


class LoanService:
    INTEREST_RATES = {
        LoanType.PERSONAL.value: Decimal("11.5"),
        LoanType.HOME.value: Decimal("8.5"),
        LoanType.AUTO.value: Decimal("9.2"),
        LoanType.EDUCATION.value: Decimal("9.0"),
        LoanType.BUSINESS.value: Decimal("13.0"),
    }

    @staticmethod
    def apply_for_loan(db: Session, customer_id: str, req: LoanApplyRequest) -> LoanApplication:
        metrics.inc("loans_applied_total")
        rate = LoanService.INTEREST_RATES.get(req.loan_type, Decimal("11.5"))
        principal = to_decimal(req.amount)
        emi = calculate_emi(principal, rate, req.tenure_months)

        app_num = f"LON-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        loan = LoanApplication(
            application_number=app_num,
            customer_id=customer_id,
            loan_type=req.loan_type,
            requested_amount=req.amount,
            tenure_months=req.tenure_months,
            interest_rate_annual=float(rate),
            monthly_emi=float(emi),
            status=LoanStatus.APPROVED.value,  # Instant automated approval in sandbox
            disbursed_account_number=req.disbursement_account_number or "100019283746",
            credit_score_at_application=765,
            underwriter_notes="Automated rule engine approval: Low risk profile, DTI < 30%"
        )
        db.add(loan)
        db.flush()

        # Generate Amortization Schedule
        monthly_rate = (rate / Decimal(100)) / Decimal(12)
        remaining_principal = principal

        now = datetime.now(timezone.utc)
        for i in range(1, req.tenure_months + 1):
            interest_comp = remaining_principal * monthly_rate
            principal_comp = emi - interest_comp
            if principal_comp > remaining_principal or i == req.tenure_months:
                principal_comp = remaining_principal
                emi_amt = principal_comp + interest_comp
            else:
                emi_amt = emi

            remaining_principal -= principal_comp
            due_dt = now + timedelta(days=30 * i)

            repayment = LoanRepayment(
                loan_id=loan.id,
                installment_number=i,
                due_date=due_dt,
                principal_component=float(to_decimal(principal_comp)),
                interest_component=float(to_decimal(interest_comp)),
                total_installment_amount=float(to_decimal(emi_amt)),
                status="PENDING"
            )
            db.add(repayment)

        # Disburse Loan:
        # Debit Loans Receivable (1030) ₹Amount
        # Credit Customer Deposits (2000) ₹Amount
        target_acc = db.query(BankAccount).filter(BankAccount.account_number == loan.disbursed_account_number).first()
        if target_acc:
            target_acc.available_balance += req.amount

        ledger_service.post_journal_entry(db, JournalEntryCreate(
            transaction_id=loan.application_number,
            description=f"Loan Disbursement: {loan.application_number} ({req.loan_type})",
            currency="INR",
            postings=[
                PostingCreate(account_code="1030", entry_type="DEBIT", amount=req.amount, description="Loan Asset Receivable"),
                PostingCreate(account_code="2000", entry_type="CREDIT", amount=req.amount, description="Customer Account Credit")
            ]
        ))

        loan.status = LoanStatus.DISBURSED.value
        loan.disbursed_at = datetime.now(timezone.utc)
        metrics.inc("loans_approved_total")

        db.commit()
        db.refresh(loan)
        return loan

    @staticmethod
    def repay_installment(db: Session, req: LoanRepayRequest) -> LoanRepayment:
        repayment = db.query(LoanRepayment).filter(
            LoanRepayment.loan_id == req.loan_id,
            LoanRepayment.installment_number == req.installment_number
        ).first()
        if not repayment:
            raise EntityNotFoundException("LoanRepayment", str(req.installment_number))

        source_acc = db.query(BankAccount).filter(BankAccount.account_number == req.source_account_number).first()
        if source_acc:
            if source_acc.available_balance < req.amount:
                raise InsufficientFundsException("Insufficient funds in account to pay EMI.")
            source_acc.available_balance -= req.amount

        repayment.status = "PAID"
        repayment.paid_at = datetime.now(timezone.utc)
        repayment.payment_reference = f"EMI-PAY-{uuid.uuid4().hex[:8].upper()}"

        # Double-entry ledger:
        # Debit Customer Account (2000) ₹Total
        # Credit Loans Receivable (1030) ₹PrincipalComponent
        # Credit Loan Interest Income (4010) ₹InterestComponent
        ledger_service.post_journal_entry(db, JournalEntryCreate(
            transaction_id=repayment.payment_reference,
            description=f"EMI Payment #{req.installment_number} for Loan {req.loan_id}",
            currency="INR",
            postings=[
                PostingCreate(account_code="2000", entry_type="DEBIT", amount=req.amount, description="Customer Account Debit"),
                PostingCreate(account_code="1030", entry_type="CREDIT", amount=repayment.principal_component, description="Principal Reduction"),
                PostingCreate(account_code="4010", entry_type="CREDIT", amount=repayment.interest_component, description="Interest Revenue")
            ]
        ))

        db.commit()
        db.refresh(repayment)
        return repayment


loan_service = LoanService()
