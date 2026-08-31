"""Dynamic Smart Payment Routing & Health Degradation Auto-Failover Engine."""

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
