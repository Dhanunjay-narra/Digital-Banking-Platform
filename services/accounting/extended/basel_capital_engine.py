"""Basel III Capital Adequacy Ratio (CAR) & Risk-Weighted Assets (RWA) Engine."""

from typing import Dict, Any, List
from decimal import Decimal


class BaselIIICalculator:
    """Calculates Tier-1 Capital, Tier-2 Capital, and Capital-to-Risk-Weighted-Assets Ratio (CRAR)."""

    RISK_WEIGHTS = {
        "CENTRAL_BANK_CASH": 0.0,
        "SOVEREIGN_BONDS": 0.0,
        "INTERBANK_AAA": 0.20,
        "RESIDENTIAL_MORTGAGES_LTV_UNDER_75": 0.35,
        "RESIDENTIAL_MORTGAGES_LTV_OVER_75": 0.50,
        "RETAIL_PERSONAL_LOANS": 0.75,
        "CREDIT_CARD_RECEIVABLES": 1.25,
        "CORPORATE_AAA": 0.20,
        "CORPORATE_BBB": 1.00,
        "CORPORATE_UNRATED": 1.00,
        "NPA_NON_PERFORMING_ASSET": 1.50,
    }

    @staticmethod
    def calculate_crar(
        tier1_common_equity: float,
        tier1_additional: float,
        tier2_subordinated_debt: float,
        asset_holdings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        total_rwa = 0.0
        rwa_breakdown = []

        for asset in asset_holdings:
            asset_type = asset.get("asset_type", "RETAIL_PERSONAL_LOANS")
            amount = float(asset.get("amount", 0.0))
            weight = BaselIIICalculator.RISK_WEIGHTS.get(asset_type, 1.0)
            weighted_amount = amount * weight
            total_rwa += weighted_amount
            rwa_breakdown.append({
                "asset_type": asset_type,
                "exposure_amount": amount,
                "risk_weight": weight,
                "risk_weighted_exposure": round(weighted_amount, 2)
            })

        total_tier1 = tier1_common_equity + tier1_additional
        total_regulatory_capital = total_tier1 + tier2_subordinated_debt

        crar_pct = (total_regulatory_capital / total_rwa * 100.0) if total_rwa > 0 else 100.0
        tier1_ratio_pct = (total_tier1 / total_rwa * 100.0) if total_rwa > 0 else 100.0

        # Regulatory minimums: Total CRAR >= 9.0% (RBI: 11.5%), Tier 1 >= 7.0%
        is_compliant = crar_pct >= 11.5 and tier1_ratio_pct >= 7.0

        return {
            "total_risk_weighted_assets_rwa": round(total_rwa, 2),
            "tier1_capital": round(total_tier1, 2),
            "tier2_capital": round(tier2_subordinated_debt, 2),
            "total_regulatory_capital": round(total_regulatory_capital, 2),
            "crar_percentage": round(crar_pct, 2),
            "tier1_capital_ratio_percentage": round(tier1_ratio_pct, 2),
            "regulatory_minimum_required": 11.5,
            "capital_adequacy_status": "COMPLIANT_WELL_CAPITALIZED" if is_compliant else "CAPITAL_DEFICIENT",
            "rwa_breakdown": rwa_breakdown
        }
