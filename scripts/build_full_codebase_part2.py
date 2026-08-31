"""Part 2 Domain Generator for FinXCore Digital Banking Platform."""

import os

def write_code_file(relative_path: str, content: str):
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {relative_path}")

def build_part2():
    # 1. Smart Payment Routing
    smart_routing_code = '''"""Dynamic Smart Payment Routing & Health Degradation Auto-Failover Engine."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


class PaymentGatewayGatewayNode:
    def __init__(self, gateway_id: str, name: str, success_rate: float, avg_latency_ms: float, cost_per_tx_bps: int):
        self.gateway_id = gateway_id
        self.name = name
        self.success_rate = success_rate
        self.avg_latency_ms = avg_latency_ms
        self.cost_per_tx_bps = cost_per_tx_bps
        self.is_healthy = True
        self.consecutive_failures = 0

    def calculate_score(self) -> float:
        if not self.is_healthy:
            return -1.0
        latency_score = max(0.0, 100.0 - (self.avg_latency_ms / 10.0))
        cost_score = max(0.0, 100.0 - (self.cost_per_tx_bps / 5.0))
        score = (self.success_rate * 0.60) + (latency_score * 0.25) + (cost_score * 0.15)
        return round(score, 2)


class SmartPaymentRouter:
    """Selects the optimal acquiring gateway dynamically based on real-time health and latency telemetry."""

    def __init__(self):
        self.nodes = [
            PaymentGatewayGatewayNode("GW_HDFC", "HDFC SmartGateway", 99.6, 65.0, 150),
            PaymentGatewayGatewayNode("GW_ICICI", "ICICI E-Pay Direct", 99.4, 72.0, 145),
            PaymentGatewayGatewayNode("GW_AXIS", "Axis Payment Switch", 98.9, 85.0, 140),
            PaymentGatewayGatewayNode("GW_SBI", "SBI Aggregator Rail", 97.8, 120.0, 120),
        ]

    def route_payment(self, payment_method: str, amount: float, preferred_rail: Optional[str] = None) -> Dict[str, Any]:
        scored_nodes = [(n, n.calculate_score()) for n in self.nodes if n.is_healthy]
        scored_nodes.sort(key=lambda x: x[1], reverse=True)

        if not scored_nodes:
            raise RuntimeError("All payment acquiring gateways are currently degraded!")

        selected_node, score = scored_nodes[0]
        backup_node = scored_nodes[1][0] if len(scored_nodes) > 1 else None

        return {
            "selected_gateway_id": selected_node.gateway_id,
            "selected_gateway_name": selected_node.name,
            "routing_score": score,
            "expected_latency_ms": selected_node.avg_latency_ms,
            "failover_backup_gateway": backup_node.name if backup_node else "None",
            "routing_decision_timestamp": datetime.now(timezone.utc).isoformat()
        }


smart_payment_router = SmartPaymentRouter()
'''
    write_code_file("services/payments/extended/smart_routing.py", smart_routing_code)

    # 2. Card Lifecycle & Tokenization
    card_lifecycle_code = '''"""Payment Card Tokenization, Virtual Provisioning & Pin Security Engine."""

from typing import Dict, Any, Optional
import hashlib
import uuid
from datetime import datetime, timezone


class CardLifecycleEngine:
    @staticmethod
    def generate_device_token(pan: str, device_id: str, wallet_provider: str = "APPLE_PAY") -> Dict[str, Any]:
        token_id = f"DPAN_{uuid.uuid4().hex[:16].upper()}"
        cryptogram = hashlib.sha256(f"{pan}:{device_id}:{token_id}".encode()).hexdigest()[:32]
        
        return {
            "token_reference": token_id,
            "token_requestor_id": wallet_provider,
            "device_id": device_id,
            "token_status": "ACTIVE_PROVISIONED",
            "token_expiry": "12/31",
            "device_cryptogram": cryptogram,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def verify_emv_pin(stored_pin_hash: str, entered_plain_pin: str, salt: str) -> bool:
        computed = hashlib.sha256((entered_plain_pin + salt).encode()).hexdigest()
        return computed == stored_pin_hash
'''
    write_code_file("services/cards/extended/card_lifecycle.py", card_lifecycle_code)

    # 3. KYB Merchant Verification
    kyb_content = '''"""Know-Your-Business (KYB) Verification & Merchant Risk Categorization Engine."""

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
'''
    write_code_file("services/merchants/extended/kyb_engine.py", kyb_content)

    # 4. Expense Categorizer & Anomaly Patterns
    expense_patterns = '''"""Machine Learning Expense Categorizer & Monthly Anomaly Pattern Classifier."""

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
'''
    write_code_file("services/expenses/extended/spending_patterns.py", expense_patterns)

    # 5. Merkle Tree Audit Verification
    merkle_tree_code = '''"""Cryptographic Merkle Tree Engine for Immutable Bank Audit Trail Integrity."""

import hashlib
from typing import List, Optional


class MerkleTree:
    """Constructs a binary hash tree over platform audit log events for verifiable tamper resistance."""

    def __init__(self, leaf_hashes: List[str]):
        self.leaves = leaf_hashes
        self.tree: List[List[str]] = []
        if leaf_hashes:
            self._build_tree()

    def _hash_pair(self, left: str, right: str) -> str:
        return hashlib.sha256((left + right).encode("utf-8")).hexdigest()

    def _build_tree(self) -> None:
        current_layer = self.leaves[:]
        self.tree.append(current_layer)
        while len(current_layer) > 1:
            next_layer = []
            for i in range(0, len(current_layer), 2):
                left = current_layer[i]
                right = current_layer[i + 1] if i + 1 < len(current_layer) else left
                next_layer.append(self._hash_pair(left, right))
            self.tree.append(next_layer)
            current_layer = next_layer

    def get_root_hash(self) -> Optional[str]:
        if not self.tree or not self.tree[-1]:
            return None
        return self.tree[-1][0]

    def verify_inclusion(self, leaf_hash: str, proof: List[str], root_hash: str) -> bool:
        current = leaf_hash
        for p in proof:
            current = self._hash_pair(current, p)
        return current == root_hash
'''
    write_code_file("finx_platform/core/audit/merkle_tree.py", merkle_tree_code)

    print("Part 2 domain extensions generated successfully!")

if __name__ == "__main__":
    build_part2()
