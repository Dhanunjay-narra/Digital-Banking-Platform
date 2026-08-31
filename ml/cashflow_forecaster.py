"""Time-Series Cashflow & Balance Forecasting Model."""

from typing import List, Dict, Any


class CashflowForecaster:
    def forecast_30_days(self, current_balance: float, avg_daily_income: float, avg_daily_expense: float) -> Dict[str, Any]:
        forecast_points: List[Dict[str, Any]] = []
        running_balance = current_balance

        for day in range(1, 31):
            daily_net = avg_daily_income - avg_daily_expense
            running_balance += daily_net
            forecast_points.append({
                "day": day,
                "projected_balance": round(running_balance, 2),
                "lower_bound_95": round(running_balance * 0.92, 2),
                "upper_bound_95": round(running_balance * 1.08, 2)
            })

        min_bal = min(p["projected_balance"] for p in forecast_points)

        return {
            "starting_balance": current_balance,
            "projected_end_balance": forecast_points[-1]["projected_balance"],
            "lowest_projected_balance": round(min_bal, 2),
            "liquidity_alert": min_bal < 5000.0,
            "forecast_days": forecast_points
        }


cashflow_forecaster = CashflowForecaster()
