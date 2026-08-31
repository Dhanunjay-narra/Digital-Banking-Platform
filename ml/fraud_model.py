"""Machine Learning Fraud & Anomaly Scoring Classifier."""

import math
from typing import Dict, Any, List


class MLFraudClassifier:
    """Statistical & Machine Learning Anomaly Detection Model."""
    def __init__(self):
        self.feature_weights = {
            "amount_z_score": 0.35,
            "velocity_1h": 0.25,
            "device_anomaly": 0.20,
            "geo_distance_km": 0.15,
            "time_of_day_risk": 0.05
        }

    def predict_risk_score(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Calculates a normalized probability [0.0, 1.0] of transaction fraud."""
        z_score = features.get("amount_z_score", 0.0)
        velocity = features.get("velocity_1h", 1.0)
        device_anom = features.get("device_anomaly", 0.0)
        geo_dist = features.get("geo_distance_km", 0.0)
        time_risk = features.get("time_of_day_risk", 0.1)

        # Sigmoidal logit combination
        logit = (
            z_score * self.feature_weights["amount_z_score"] +
            (velocity / 10.0) * self.feature_weights["velocity_1h"] +
            device_anom * self.feature_weights["device_anomaly"] +
            min(1.0, geo_dist / 1000.0) * self.feature_weights["geo_distance_km"] +
            time_risk * self.feature_weights["time_of_day_risk"] - 0.5
        )

        probability = 1.0 / (1.0 + math.exp(-logit * 3))
        risk_score_100 = round(probability * 100, 2)

        return {
            "fraud_probability": round(probability, 4),
            "ml_risk_score": risk_score_100,
            "is_anomaly": risk_score_100 >= 65.0,
            "model_version": "finx_fraud_ensemble_v2.4"
        }


ml_fraud_classifier = MLFraudClassifier()
