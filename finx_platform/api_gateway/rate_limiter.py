"""Sliding Window Rate Limiter Middleware."""

import time
from collections import defaultdict
from typing import Dict, List
from finx_platform.config.settings import settings
from finx_platform.common.exceptions import FinTechException


class RateLimiter:
    def __init__(self, max_requests: int = settings.RATE_LIMIT_REQUESTS, window_seconds: int = settings.RATE_LIMIT_WINDOW_SECONDS):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.client_records: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        # Clean older entries
        self.client_records[client_ip] = [t for t in self.client_records[client_ip] if t > window_start]
        if len(self.client_records[client_ip]) >= self.max_requests:
            return False
        self.client_records[client_ip].append(now)
        return True


rate_limiter = RateLimiter()
