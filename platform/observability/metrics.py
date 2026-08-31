"""Real-time Financial Platform Metrics Collector."""

import time
from typing import Dict, Any


class MetricsCollector:
    def __init__(self):
        self.counters: Dict[str, int] = {
            "transactions_initiated_total": 0,
            "transactions_successful_total": 0,
            "transactions_failed_total": 0,
            "fraud_cases_detected_total": 0,
            "loans_applied_total": 0,
            "loans_approved_total": 0,
            "upi_payments_total": 0,
            "gateway_payments_total": 0,
            "wallet_topups_total": 0,
            "reconciliation_breaks_total": 0,
        }
        self.gauges: Dict[str, float] = {
            "active_users_count": 0.0,
            "total_deposits_volume": 0.0,
            "total_loans_disbursed_volume": 0.0,
            "platform_uptime_seconds": time.time(),
        }

    def inc(self, counter_name: str, value: int = 1):
        if counter_name not in self.counters:
            self.counters[counter_name] = 0
        self.counters[counter_name] += value

    def set_gauge(self, gauge_name: str, value: float):
        self.gauges[gauge_name] = value

    def snapshot(self) -> Dict[str, Any]:
        return {
            "counters": self.counters.copy(),
            "gauges": self.gauges.copy(),
            "uptime_seconds": round(time.time() - self.gauges["platform_uptime_seconds"], 2)
        }


metrics = MetricsCollector()
