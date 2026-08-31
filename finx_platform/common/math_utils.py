"""Financial Mathematics and Decimal Precision Utilities."""

from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from typing import Union


def to_decimal(value: Union[str, int, float, Decimal], places: int = 2) -> Decimal:
    """Converts a value to exact monetary Decimal with fixed precision."""
    if isinstance(value, float):
        value = str(value)
    d = Decimal(str(value))
    exp = Decimal("10") ** -places
    return d.quantize(exp, rounding=ROUND_HALF_UP)


def calculate_emi(principal: Decimal, annual_interest_rate_percent: Decimal, tenure_months: int) -> Decimal:
    """Standard reducing balance EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)"""
    if annual_interest_rate_percent == 0:
        return to_decimal(principal / tenure_months)

    monthly_rate = (annual_interest_rate_percent / Decimal(100)) / Decimal(12)
    one_plus_r = Decimal(1) + monthly_rate
    pow_factor = one_plus_r ** tenure_months

    numerator = principal * monthly_rate * pow_factor
    denominator = pow_factor - Decimal(1)

    emi = numerator / denominator
    return to_decimal(emi)


def calculate_simple_interest(principal: Decimal, annual_rate_percent: Decimal, days: int) -> Decimal:
    interest = (principal * annual_rate_percent * Decimal(days)) / (Decimal(100) * Decimal(365))
    return to_decimal(interest)
