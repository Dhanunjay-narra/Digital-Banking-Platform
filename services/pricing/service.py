"""Centralized Pricing & Fee Engine."""

from typing import Dict, Any


class PricingEngine:
    @staticmethod
    def calculate_fee(service_type: str, amount: float, customer_segment: str = "RETAIL_STANDARD") -> Dict[str, Any]:
        """Centralized pricing rules preventing duplicated fee calculations."""
        base_fee = 0.0
        fee_rate_percent = 0.0

        if service_type == "IMPS_TRANSFER":
            base_fee = 5.0 if amount <= 10000 else 15.0
        elif service_type == "NEFT_TRANSFER" or service_type == "UPI_PAYMENT":
            base_fee = 0.0  # Free as per regulatory mandate
        elif service_type == "MERCHANT_MDR":
            fee_rate_percent = 1.8
            base_fee = amount * (fee_rate_percent / 100)
        elif service_type == "INTERNATIONAL_CARD":
            fee_rate_percent = 3.5
            base_fee = amount * (fee_rate_percent / 100)
        elif service_type == "LOAN_PROCESSING":
            fee_rate_percent = 1.0
            base_fee = max(1000.0, amount * (fee_rate_percent / 100))

        # Premium waiver
        discount_percent = 50.0 if customer_segment in ["PREMIUM", "HNI", "WEALTH"] else 0.0
        final_fee = base_fee * (1.0 - (discount_percent / 100))
        gst = round(final_fee * 0.18, 2)  # 18% standard GST

        return {
            "service_type": service_type,
            "base_fee": round(base_fee, 2),
            "discount_percent": discount_percent,
            "net_fee": round(final_fee, 2),
            "gst_tax_18_pct": gst,
            "total_charge": round(final_fee + gst, 2)
        }


pricing_engine = PricingEngine()
