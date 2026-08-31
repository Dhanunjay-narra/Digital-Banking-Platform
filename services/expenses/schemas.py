"""Expense Management Pydantic Schemas."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ExpenseCreateRequest(BaseModel):
    category: str = "FOOD_DINING"
    amount: float = Field(..., gt=0)
    entry_type: str = Field("EXPENSE", pattern="^(INCOME|EXPENSE)$")
    merchant_name: Optional[str] = None
    description: str


class BudgetGoalCreate(BaseModel):
    category: str
    monthly_budget_limit: float = Field(..., gt=0)


class ExpenseSummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    spending_by_category: Dict[str, float]
    budget_utilization: List[Dict[str, Any]]
