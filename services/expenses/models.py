"""Expense Management & Personal Finance Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from platform.common.database import Base
from platform.common.base_model import generate_uuid, TimestampMixin


class ExpenseCategory(str, Enum):
    FOOD_DINING = "FOOD_DINING"
    SHOPPING = "SHOPPING"
    UTILITIES_BILLS = "UTILITIES_BILLS"
    TRAVEL_COMMUTE = "TRAVEL_COMMUTE"
    ENTERTAINMENT = "ENTERTAINMENT"
    HEALTHCARE = "HEALTHCARE"
    INVESTMENTS = "INVESTMENTS"
    SALARY_INCOME = "SALARY_INCOME"
    OTHERS = "OTHERS"


class ExpenseRecord(Base, TimestampMixin):
    __tablename__ = "expense_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    category = Column(String(50), default=ExpenseCategory.OTHERS.value, nullable=False)
    amount = Column(Float, nullable=False)
    entry_type = Column(String(10), default="EXPENSE")  # INCOME or EXPENSE
    merchant_name = Column(String(150), nullable=True)
    description = Column(String(255), nullable=False)
    transaction_date = Column(DateTime, nullable=False)


class BudgetGoal(Base, TimestampMixin):
    __tablename__ = "budget_goals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    category = Column(String(50), nullable=False)
    monthly_budget_limit = Column(Float, nullable=False)
    current_spent = Column(Float, default=0.0)
