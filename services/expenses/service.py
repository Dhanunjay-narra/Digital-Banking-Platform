"""Personal Finance Management & Auto Categorization Service."""

from datetime import datetime, timezone
from typing import Dict, Any, List
from collections import defaultdict
from sqlalchemy.orm import Session
from services.expenses.models import ExpenseRecord, BudgetGoal, ExpenseCategory
from services.expenses.schemas import ExpenseCreateRequest, ExpenseSummaryResponse


class ExpenseService:
    CATEGORIZATION_RULES = {
        "swiggy": ExpenseCategory.FOOD_DINING.value,
        "zomato": ExpenseCategory.FOOD_DINING.value,
        "starbucks": ExpenseCategory.FOOD_DINING.value,
        "amazon": ExpenseCategory.SHOPPING.value,
        "flipkart": ExpenseCategory.SHOPPING.value,
        "myntra": ExpenseCategory.SHOPPING.value,
        "uber": ExpenseCategory.TRAVEL_COMMUTE.value,
        "ola": ExpenseCategory.TRAVEL_COMMUTE.value,
        "netflix": ExpenseCategory.ENTERTAINMENT.value,
        "spotify": ExpenseCategory.ENTERTAINMENT.value,
        "electricity": ExpenseCategory.UTILITIES_BILLS.value,
        "broadband": ExpenseCategory.UTILITIES_BILLS.value,
        "pharmacy": ExpenseCategory.HEALTHCARE.value,
        "apollo": ExpenseCategory.HEALTHCARE.value,
        "salary": ExpenseCategory.SALARY_INCOME.value,
    }

    @staticmethod
    def auto_categorize(text: str) -> str:
        lower = text.lower()
        for keyword, cat in ExpenseService.CATEGORIZATION_RULES.items():
            if keyword in lower:
                return cat
        return ExpenseCategory.OTHERS.value

    @staticmethod
    def record_expense(db: Session, customer_id: str, req: ExpenseCreateRequest) -> ExpenseRecord:
        cat = req.category
        if not cat or cat == "OTHERS":
            cat = ExpenseService.auto_categorize(f"{req.merchant_name or ''} {req.description}")

        rec = ExpenseRecord(
            customer_id=customer_id,
            category=cat,
            amount=req.amount,
            entry_type=req.entry_type,
            merchant_name=req.merchant_name,
            description=req.description,
            transaction_date=datetime.now(timezone.utc)
        )
        db.add(rec)

        # Update budget spent
        if req.entry_type == "EXPENSE":
            bg = db.query(BudgetGoal).filter(BudgetGoal.customer_id == customer_id, BudgetGoal.category == cat).first()
            if bg:
                bg.current_spent += req.amount

        db.commit()
        db.refresh(rec)
        return rec

    @staticmethod
    def get_summary(db: Session, customer_id: str) -> ExpenseSummaryResponse:
        records = db.query(ExpenseRecord).filter(ExpenseRecord.customer_id == customer_id).all()
        if not records:
            # Seed demo expense entries
            samples = [
                ("Salary Credit - FinX Technologies", 150000.0, "INCOME", "SALARY_INCOME"),
                ("Swiggy Gourmet Dinner", 1250.0, "EXPENSE", "FOOD_DINING"),
                ("Amazon Tech Electronics", 8500.0, "EXPENSE", "SHOPPING"),
                ("Bescom Electricity Bill", 2400.0, "EXPENSE", "UTILITIES_BILLS"),
                ("Uber Daily Commute", 650.0, "EXPENSE", "TRAVEL_COMMUTE"),
                ("Netflix 4K Subscription", 649.0, "EXPENSE", "ENTERTAINMENT"),
            ]
            for desc, amt, e_type, cat in samples:
                ExpenseService.record_expense(db, customer_id, ExpenseCreateRequest(
                    category=cat,
                    amount=amt,
                    entry_type=e_type,
                    description=desc
                ))
            records = db.query(ExpenseRecord).filter(ExpenseRecord.customer_id == customer_id).all()

        tot_inc = sum(r.amount for r in records if r.entry_type == "INCOME")
        tot_exp = sum(r.amount for r in records if r.entry_type == "EXPENSE")
        cat_map = defaultdict(float)
        for r in records:
            if r.entry_type == "EXPENSE":
                cat_map[r.category] += r.amount

        budgets = db.query(BudgetGoal).filter(BudgetGoal.customer_id == customer_id).all()
        budget_util = [
            {"category": b.category, "limit": b.monthly_budget_limit, "spent": b.current_spent, "percent": round((b.current_spent / b.monthly_budget_limit * 100), 1) if b.monthly_budget_limit > 0 else 0}
            for b in budgets
        ]

        return ExpenseSummaryResponse(
            total_income=round(tot_inc, 2),
            total_expenses=round(tot_exp, 2),
            net_savings=round(tot_inc - tot_exp, 2),
            spending_by_category=dict(cat_map),
            budget_utilization=budget_util
        )


expense_service = ExpenseService()
