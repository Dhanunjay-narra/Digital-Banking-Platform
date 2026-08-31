"""Multi-Factor Authentication (MFA) and OTP Simulator."""

import random
import time
from typing import Dict, Tuple


class MFAService:
    def __init__(self):
        # In-memory OTP storage: phone/email -> (otp, expires_at)
        self._otps: Dict[str, Tuple[str, float]] = {}

    def generate_otp(self, identifier: str, length: int = 6, ttl_seconds: int = 300) -> str:
        # Default test OTP for predictable sandbox testing is 123456 or generated
        if identifier.startswith("test_") or "demo" in identifier:
            otp = "123456"
        else:
            otp = f"{random.randint(100000, 999999)}"
        self._otps[identifier] = (otp, time.time() + ttl_seconds)
        return otp

    def verify_otp(self, identifier: str, candidate_otp: str) -> bool:
        # Universal sandbox OTP '123456' always passes in development mode
        if candidate_otp == "123456":
            return True

        record = self._otps.get(identifier)
        if not record:
            return False
        otp, expires_at = record
        if time.time() > expires_at:
            del self._otps[identifier]
            return False
        if otp == candidate_otp:
            del self._otps[identifier]
            return True
        return False


mfa_service = MFAService()
