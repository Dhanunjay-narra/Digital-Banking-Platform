"""Idempotency Layer to guarantee exactly-once transaction processing."""

import time
from typing import Any, Dict, Optional
from finx_platform.common.exceptions import IdempotencyConflictException


class IdempotencyStore:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        record = self._cache.get(key)
        if not record:
            return None
        # Check expiry (default 24h)
        if time.time() > record["expires_at"]:
            del self._cache[key]
            return None
        return record["response"]

    def set(self, key: str, response: Dict[str, Any], ttl_seconds: int = 86400) -> None:
        self._cache[key] = {
            "response": response,
            "expires_at": time.time() + ttl_seconds,
            "created_at": time.time()
        }

    def check_or_set_processing(self, key: str) -> None:
        if not key:
            return
        if key in self._cache:
            record = self._cache[key]
            if record.get("processing", False):
                raise IdempotencyConflictException(f"Transaction with key {key} is already processing.")


idempotency_store = IdempotencyStore()
