"""Quantitative Portfolio Analytics, Sharpe Ratio & Mean-Variance Optimization."""

from typing import List, Dict, Any
import math


class PortfolioAnalyticsEngine:
    """Calculates risk-adjusted performance metrics for customer investment portfolios."""

    @staticmethod
    def calculate_sharpe_ratio(annualized_return: float, risk_free_rate: float = 6.5, portfolio_volatility: float = 12.0) -> float:
        if portfolio_volatility <= 0:
            return 0.0
        excess_return = annualized_return - risk_free_rate
        return round(excess_return / portfolio_volatility, 3)

    @staticmethod
    def calculate_var_monte_carlo(portfolio_value: float, daily_volatility: float = 0.012, confidence_level: float = 0.95, time_horizon_days: int = 1) -> Dict[str, Any]:
        """Value at Risk (VaR) calculation using parametric distribution."""
        z_score = 1.645 if confidence_level == 0.95 else 2.326  # 95% vs 99%
        var_amount = portfolio_value * z_score * daily_volatility * math.sqrt(time_horizon_days)

        return {
            "portfolio_value": portfolio_value,
            "confidence_level_pct": confidence_level * 100,
            "time_horizon_days": time_horizon_days,
            "value_at_risk_amount": round(var_amount, 2),
            "max_expected_loss_pct": round((var_amount / portfolio_value) * 100, 2)
        }

    @staticmethod
    def suggest_asset_allocation_rebalance(
        current_allocations: Dict[str, float],  # e.g., {"EQUITY": 75.0, "DEBT": 15.0, "GOLD": 10.0}
        target_risk_profile: str = "MODERATE_BALANCED"
    ) -> Dict[str, Any]:
        """Calculates rebalancing delta to restore target portfolio weights."""
        targets = {
            "CONSERVATIVE": {"EQUITY": 25.0, "DEBT": 65.0, "GOLD": 10.0},
            "MODERATE_BALANCED": {"EQUITY": 55.0, "DEBT": 35.0, "GOLD": 10.0},
            "AGGRESSIVE_GROWTH": {"EQUITY": 80.0, "DEBT": 15.0, "GOLD": 5.0}
        }.get(target_risk_profile, {"EQUITY": 55.0, "DEBT": 35.0, "GOLD": 10.0})

        deltas = {}
        for asset, target_pct in targets.items():
            current_pct = current_allocations.get(asset, 0.0)
            diff = round(target_pct - current_pct, 1)
            action = "BUY" if diff > 0 else "SELL" if diff < 0 else "HOLD"
            deltas[asset] = {
                "current_percent": current_pct,
                "target_percent": target_pct,
                "rebalance_action": action,
                "delta_percent": abs(diff)
            }

        return {
            "risk_profile": target_risk_profile,
            "rebalance_recommendations": deltas
        }
