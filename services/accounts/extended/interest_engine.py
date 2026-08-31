"""Daily Compound Interest Accrual & Tiered Rate Engine."""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date, timedelta, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class TieredInterestBracket(BaseModel):
    min_balance: float
    max_balance: Optional[float]
    annual_interest_rate: float  # Percentage, e.g. 4.0 for 4%


class AccountInterestLedger:
    """Computes daily product method interest and monthly capitalizations."""
    
    DEFAULT_SAVINGS_TIERS = [
        TieredInterestBracket(min_balance=0.0, max_balance=100000.0, annual_interest_rate=3.5),
        TieredInterestBracket(min_balance=100000.0, max_balance=1000000.0, annual_interest_rate=4.25),
        TieredInterestBracket(min_balance=1000000.0, max_balance=5000000.0, annual_interest_rate=6.0),
        TieredInterestBracket(min_balance=5000000.0, max_balance=None, annual_interest_rate=7.0),
    ]

    @staticmethod
    def calculate_daily_interest(closing_balance: float, tiers: Optional[List[TieredInterestBracket]] = None) -> float:
        if closing_balance <= 0:
            return 0.0
        
        tier_list = tiers or AccountInterestLedger.DEFAULT_SAVINGS_TIERS
        total_daily_interest = Decimal("0.0")
        balance_dec = Decimal(str(closing_balance))

        for tier in tier_list:
            t_min = Decimal(str(tier.min_balance))
            t_max = Decimal(str(tier.max_balance)) if tier.max_balance is not None else None
            rate = Decimal(str(tier.annual_interest_rate)) / Decimal("100")
            daily_rate = rate / Decimal("365")

            if balance_dec > t_min:
                if t_max is not None:
                    slab_amt = min(balance_dec - t_min, t_max - t_min)
                else:
                    slab_amt = balance_dec - t_min
                
                slab_daily = slab_amt * daily_rate
                total_daily_interest += slab_daily

        return float(total_daily_interest.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))

    @staticmethod
    def calculate_monthly_accrual(daily_balances: List[float], tiers: Optional[List[TieredInterestBracket]] = None) -> Dict[str, Any]:
        total_accrued = 0.0
        daily_breakdown = []

        for idx, bal in enumerate(daily_balances):
            day_interest = AccountInterestLedger.calculate_daily_interest(bal, tiers)
            total_accrued += day_interest
            daily_breakdown.append({
                "day": idx + 1,
                "closing_balance": bal,
                "daily_interest_accrued": day_interest
            })

        rounded_total = round(total_accrued, 2)
        avg_monthly_balance = sum(daily_balances) / len(daily_balances) if daily_balances else 0.0

        return {
            "days_evaluated": len(daily_balances),
            "average_monthly_balance": round(avg_monthly_balance, 2),
            "total_interest_to_credit": rounded_total,
            "daily_accruals": daily_breakdown
        }

    @staticmethod
    def calculate_amb_shortfall_penalty(avg_monthly_balance: float, required_amb: float = 10000.0) -> Dict[str, Any]:
        if avg_monthly_balance >= required_amb:
            return {
                "has_shortfall": False,
                "shortfall_amount": 0.0,
                "penalty_charge": 0.0,
                "gst_charge": 0.0,
                "total_charge": 0.0
            }
        
        shortfall = required_amb - avg_monthly_balance
        shortfall_pct = (shortfall / required_amb) * 100.0

        if shortfall_pct <= 25.0:
            base_penalty = 150.0
        elif shortfall_pct <= 50.0:
            base_penalty = 300.0
        elif shortfall_pct <= 75.0:
            base_penalty = 450.0
        else:
            base_penalty = 600.0

        gst = round(base_penalty * 0.18, 2)

        return {
            "has_shortfall": True,
            "shortfall_amount": round(shortfall, 2),
            "shortfall_percentage": round(shortfall_pct, 1),
            "penalty_charge": base_penalty,
            "gst_charge": gst,
            "total_charge": round(base_penalty + gst, 2)
        }
