"""Know-Your-Business (KYB) Verification & Merchant Risk Categorization Engine."""

from typing import Dict, Any, List
import re


class KYBMerchantValidator:
    GST_REGEX = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
    PAN_REGEX = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"

    MCC_RISK_RATINGS = {
        "5411": {"category": "Grocery Stores / Supermarkets", "risk": "LOW", "settlement_cycle": "T+0"},
        "5812": {"category": "Restaurants & Dining", "risk": "LOW", "settlement_cycle": "T+0"},
        "5732": {"category": "Electronic Sales", "risk": "MEDIUM", "settlement_cycle": "T+1"},
        "7995": {"category": "Betting / Gambling", "risk": "PROHIBITED", "settlement_cycle": "BLOCKED"},
        "6051": {"category": "Crypto / Quasi-Cash", "risk": "HIGH", "settlement_cycle": "T+2"},
    }

    @staticmethod
    def validate_kyb(legal_business_name: str, gstin: str, pan: str, mcc: str) -> Dict[str, Any]:
        gst_valid = bool(re.match(KYBMerchantValidator.GST_REGEX, gstin.strip().upper()))
        pan_valid = bool(re.match(KYBMerchantValidator.PAN_REGEX, pan.strip().upper()))

        mcc_info = KYBMerchantValidator.MCC_RISK_RATINGS.get(mcc, {
            "category": "General Merchant Retail",
            "risk": "MEDIUM",
            "settlement_cycle": "T+1"
        })

        is_approved = gst_valid and pan_valid and mcc_info["risk"] != "PROHIBITED"

        return {
            "legal_name": legal_business_name,
            "gstin_valid": gst_valid,
            "pan_valid": pan_valid,
            "mcc": mcc,
            "mcc_category": mcc_info["category"],
            "risk_rating": mcc_info["risk"],
            "assigned_settlement_cycle": mcc_info["settlement_cycle"],
            "kyb_status": "APPROVED" if is_approved else "REJECTED_OR_FLAGGED"
        }
