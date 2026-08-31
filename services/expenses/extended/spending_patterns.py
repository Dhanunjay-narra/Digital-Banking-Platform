"""Machine Learning Expense Categorizer & Monthly Anomaly Pattern Classifier."""

from typing import List, Dict, Any


class ExpensePatternClassifier:
    KEYWORD_CATEGORY_MAP = {
        "swiggy": "FOOD_AND_DINING",
        "zomato": "FOOD_AND_DINING",
        "starbucks": "FOOD_AND_DINING",
        "uber": "TRANSPORTATION",
        "ola": "TRANSPORTATION",
        "fuel": "TRANSPORTATION",
        "petrol": "TRANSPORTATION",
        "amazon": "SHOPPING_AND_ECOMMERCE",
        "flipkart": "SHOPPING_AND_ECOMMERCE",
        "myntra": "SHOPPING_AND_ECOMMERCE",
        "netflix": "ENTERTAINMENT_AND_SUBSCRIPTIONS",
        "spotify": "ENTERTAINMENT_AND_SUBSCRIPTIONS",
        "hotstar": "ENTERTAINMENT_AND_SUBSCRIPTIONS",
        "apollo": "HEALTHCARE_AND_WELLNESS",
        "pharmacy": "HEALTHCARE_AND_WELLNESS",
        "bescom": "UTILITIES_AND_BILLS",
        "airtel": "UTILITIES_AND_BILLS"
    }

    @staticmethod
    def categorize_description(description: str) -> str:
        desc_lower = description.lower()
        for kw, cat in ExpensePatternClassifier.KEYWORD_CATEGORY_MAP.items():
            if kw in desc_lower:
                return cat
        return "GENERAL_MISCELLANEOUS"

    @staticmethod
    def detect_category_anomalies(monthly_spend_by_cat: Dict[str, float], historical_avg_by_cat: Dict[str, float]) -> List[Dict[str, Any]]:
        anomalies = []
        for cat, current_spend in monthly_spend_by_cat.items():
            hist_avg = historical_avg_by_cat.get(cat, current_spend)
            if hist_avg > 0:
                surge_pct = ((current_spend - hist_avg) / hist_avg) * 100.0
                if surge_pct >= 40.0 and (current_spend - hist_avg) >= 2000.0:
                    anomalies.append({
                        "category": cat,
                        "current_spend": current_spend,
                        "historical_average": hist_avg,
                        "surge_percentage": round(surge_pct, 1),
                        "alert_severity": "HIGH" if surge_pct >= 75.0 else "MEDIUM"
                    })
        return anomalies
