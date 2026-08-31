"""Payment Card Tokenization, Virtual Provisioning & Pin Security Engine."""

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
