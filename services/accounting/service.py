"""Financial Accounting & Statements Generator (P&L, Balance Sheet)."""

from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from services.ledger.models import LedgerAccount, AccountType
from services.ledger.service import ledger_service


class AccountingService:
    @staticmethod
    def get_financial_statements(db: Session) -> Dict[str, Any]:
        ledger_service.initialize_chart_of_accounts(db)
        accounts = db.query(LedgerAccount).all()

        assets: List[Dict[str, Any]] = []
        liabilities: List[Dict[str, Any]] = []
        equity: List[Dict[str, Any]] = []
        revenue: List[Dict[str, Any]] = []
        expenses: List[Dict[str, Any]] = []

        total_assets = 0.0
        total_liabilities = 0.0
        total_equity = 0.0
        total_revenue = 0.0
        total_expenses = 0.0

        for a in accounts:
            item = {"code": a.account_code, "name": a.account_name, "balance": round(a.balance, 2)}
            if a.account_type == AccountType.ASSET.value:
                assets.append(item)
                total_assets += a.balance
            elif a.account_type == AccountType.LIABILITY.value:
                liabilities.append(item)
                total_liabilities += a.balance
            elif a.account_type == AccountType.EQUITY.value:
                equity.append(item)
                total_equity += a.balance
            elif a.account_type == AccountType.REVENUE.value:
                revenue.append(item)
                total_revenue += a.balance
            elif a.account_type == AccountType.EXPENSE.value:
                expenses.append(item)
                total_expenses += a.balance

        net_profit = round(total_revenue - total_expenses, 2)

        return {
            "period": f"FY {datetime.now(timezone.utc).year}-{datetime.now(timezone.utc).year + 1}",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "profit_and_loss": {
                "revenue_items": revenue,
                "total_revenue": round(total_revenue, 2),
                "expense_items": expenses,
                "total_expenses": round(total_expenses, 2),
                "net_profit_loss": net_profit
            },
            "balance_sheet": {
                "assets": assets,
                "total_assets": round(total_assets, 2),
                "liabilities": liabilities,
                "total_liabilities": round(total_liabilities, 2),
                "equity": equity,
                "total_equity": round(total_equity, 2),
                "is_balanced": abs(total_assets - (total_liabilities + total_equity + net_profit)) < 1.0
            }
        }


accounting_service = AccountingService()
