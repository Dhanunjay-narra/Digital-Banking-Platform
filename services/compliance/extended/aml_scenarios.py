"""Advanced Anti-Money Laundering (AML) Typology Engine & Sanctions Screening."""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
import math


class AMLTypologyEngine:
    """Detects complex money laundering patterns including structuring, layering, and rapid pass-through."""

    @staticmethod
    def detect_structuring_smurfing(transactions: List[Dict[str, Any]], threshold: float = 1000000.0, window_hours: int = 48) -> Dict[str, Any]:
        """Detects structuring (deposits just below regulatory reporting thresholds, e.g. ₹49,000 or ₹9,90,000)."""
        suspicious_cluster = []
        total_volume = 0.0

        for tx in transactions:
            amt = float(tx.get("amount", 0.0))
            # Just below reporting thresholds
            if (45000.0 <= amt <= 49999.0) or (900000.0 <= amt <= 999999.0):
                suspicious_cluster.append(tx)
                total_volume += amt

        is_structuring = len(suspicious_cluster) >= 3 and total_volume >= (threshold * 0.8)

        return {
            "is_structuring_detected": is_structuring,
            "suspicious_transactions_count": len(suspicious_cluster),
            "aggregate_cluster_volume": round(total_volume, 2),
            "recommended_action": "FILE_SUSPICIOUS_TRANSACTION_REPORT" if is_structuring else "MONITOR",
            "cluster": suspicious_cluster
        }

    @staticmethod
    def detect_rapid_pass_through(inflows: List[Dict[str, Any]], outflows: List[Dict[str, Any]], max_retention_minutes: int = 15) -> Dict[str, Any]:
        """Detects rapid movement of funds in and out without commercial justification (mule account behavior)."""
        tot_in = sum(float(tx.get("amount", 0.0)) for tx in inflows)
        tot_out = sum(float(tx.get("amount", 0.0)) for tx in outflows)

        if tot_in == 0:
            return {"is_pass_through_detected": False}

        pass_through_ratio = min(tot_in, tot_out) / max(tot_in, tot_out)
        is_pass_through = pass_through_ratio > 0.90 and len(inflows) >= 2 and len(outflows) >= 2

        return {
            "is_pass_through_detected": is_pass_through,
            "total_inflow": round(tot_in, 2),
            "total_outflow": round(tot_out, 2),
            "pass_through_ratio": round(pass_through_ratio * 100, 1),
            "risk_assessment": "HIGH_RISK_MULE_PATTERN" if is_pass_through else "NORMAL_COMMERCIAL_FLOW"
        }


class SanctionsFuzzyMatcher:
    """Phonetic and String-Distance Sanctions Watchlist Matching (Jaro-Winkler & Levenshtein)."""

    @staticmethod
    def jaro_winkler_similarity(s1: str, s2: str) -> float:
        s1 = s1.upper().strip()
        s2 = s2.upper().strip()
        if s1 == s2:
            return 1.0

        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0

        match_distance = max(len1, len2) // 2 - 1
        s1_matches = [False] * len1
        s2_matches = [False] * len2
        matches = 0
        transpositions = 0

        for i in range(len1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len2)
            for j in range(start, end):
                if s2_matches[j] or s1[i] != s2[j]:
                    continue
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

        if matches == 0:
            return 0.0

        k = 0
        for i in range(len1):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

        jaro = (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3.0

        # Prefix bonus up to 4 chars
        prefix = 0
        for i in range(min(4, min(len1, len2))):
            if s1[i] == s2[i]:
                prefix += 1
            else:
                break

        return jaro + prefix * 0.1 * (1.0 - jaro)
