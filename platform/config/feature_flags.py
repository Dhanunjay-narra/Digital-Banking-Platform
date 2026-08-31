"""Feature Flags management for gradual rollout and domain toggling."""

from typing import Dict


class FeatureFlagManager:
    def __init__(self):
        self._flags: Dict[str, bool] = {
            "mfa_enforcement": True,
            "biometric_auth": True,
            "instant_settlement": True,
            "upi_simulator": True,
            "real_time_fraud_scoring": True,
            "automated_loan_underwriting": True,
            "multi_rail_reconciliation": True,
            "ai_spending_insights": True,
            "virtual_card_issuance": True,
            "crypto_rail_sandbox": False,
            "dark_mode_default": False,
        }

    def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        return self._flags.get(flag_name, default)

    def set_flag(self, flag_name: str, enabled: bool) -> None:
        self._flags[flag_name] = enabled

    def get_all_flags(self) -> Dict[str, bool]:
        return self._flags.copy()


feature_flags = FeatureFlagManager()
