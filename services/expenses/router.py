"""Expense & Budget API Endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.expenses.schemas import ExpenseCreateRequest, BudgetGoalCreate, ExpenseSummaryResponse
from services.expenses.service import expense_service
from services.expenses.models import ExpenseRecord, BudgetGoal

router = APIRouter(prefix="/expenses", tags=["Personal Finance & Expenses"])


@router.get("/summary", response_model=ExpenseSummaryResponse)
def get_expense_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return expense_service.get_summary(db, customer.id)


@router.post("", response_model=None)
def add_expense(req: ExpenseCreateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    rec = expense_service.record_expense(db, customer.id, req)
    return {"success": True, "id": rec.id, "category": rec.category, "amount": rec.amount}


@router.post("/budgets")
def set_budget(req: BudgetGoalCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    bg = db.query(BudgetGoal).filter(BudgetGoal.customer_id == customer.id, BudgetGoal.category == req.category).first()
    if not bg:
        bg = BudgetGoal(customer_id=customer.id, category=req.category, monthly_budget_limit=req.monthly_budget_limit)
        db.add(bg)
    else:
        bg.monthly_budget_limit = req.monthly_budget_limit
    db.commit()
    return {"success": True, "message": f"Budget for {req.category} updated to ₹{req.monthly_budget_limit}"}
