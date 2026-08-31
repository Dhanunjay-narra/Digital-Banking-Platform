"""High-Throughput 4-Way Financial Reconciliation Engine."""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
from decimal import Decimal


class FourWayReconciliationMatcher:
    """Reconciles 4 distinct financial rails:
    1. Core Banking Ledger (Internal Source of Truth)
    2. Payment Gateway Transaction Logs (E-Commerce Inflows)
    3. National Payment Switch / NPCI / VISA / Mastercard Logs
    4. Settlement Bank Clearing Statement
    """

    @staticmethod
    def match_records(
        core_records: List[Dict[str, Any]],
        gateway_records: List[Dict[str, Any]],
        switch_records: List[Dict[str, Any]],
        bank_clearing_records: List[Dict[str, Any]],
        amount_tolerance: float = 0.01
    ) -> Dict[str, Any]:
        matched_groups = []
        breaks = []

        gw_map = {r["reference"]: r for r in gateway_records}
        sw_map = {r["reference"]: r for r in switch_records}
        bank_map = {r["reference"]: r for r in bank_clearing_records}

        for core in core_records:
            ref = core["reference"]
            core_amt = float(core["amount"])

            gw = gw_map.get(ref)
            sw = sw_map.get(ref)
            bank = bank_map.get(ref)

            # Check 4-way consistency
            is_matched = True
            mismatch_reasons = []

            if not gw:
                is_matched = False
                mismatch_reasons.append("Missing in Payment Gateway")
            elif abs(float(gw["amount"]) - core_amt) > amount_tolerance:
                is_matched = False
                mismatch_reasons.append(f"Amount mismatch in Gateway: {gw['amount']} vs {core_amt}")

            if not sw:
                is_matched = False
                mismatch_reasons.append("Missing in Switching Rail")
            elif abs(float(sw["amount"]) - core_amt) > amount_tolerance:
                is_matched = False
                mismatch_reasons.append(f"Amount mismatch in Switch: {sw['amount']} vs {core_amt}")

            if not bank:
                is_matched = False
                mismatch_reasons.append("Missing in Bank Clearing Statement")
            elif abs(float(bank["amount"]) - core_amt) > amount_tolerance:
                is_matched = False
                mismatch_reasons.append(f"Amount mismatch in Bank Statement: {bank['amount']} vs {core_amt}")

            if is_matched:
                matched_groups.append({
                    "reference": ref,
                    "amount": core_amt,
                    "status": "RECONCILED_MATCHED",
                    "matched_at": datetime.now(timezone.utc).isoformat()
                })
            else:
                breaks.append({
                    "reference": ref,
                    "core_amount": core_amt,
                    "reasons": mismatch_reasons,
                    "status": "UNRECONCILED_BREAK",
                    "severity": "CRITICAL" if not bank else "MEDIUM"
                })

        total_tx = len(core_records)
        match_rate = (len(matched_groups) / total_tx * 100.0) if total_tx > 0 else 100.0

        return {
            "total_core_transactions": total_tx,
            "reconciled_matches_count": len(matched_groups),
            "breaks_count": len(breaks),
            "match_rate_percentage": round(match_rate, 2),
            "status": "CLEAN" if len(breaks) == 0 else "EXCEPTIONS_PENDING",
            "matched_groups": matched_groups,
            "breaks": breaks
        }
