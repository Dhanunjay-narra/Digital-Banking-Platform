"""Core FinTech Custom Exceptions."""

from typing import Any, Dict, Optional


class FinTechException(Exception):
    """Base exception for all FinXCore banking errors."""
    def __init__(self, message: str, code: str = "FINTECH_ERROR", status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class InsufficientFundsException(FinTechException):
    def __init__(self, message: str = "Insufficient available funds for transaction", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="INSUFFICIENT_FUNDS", status_code=400, details=details)


class AccountFrozenException(FinTechException):
    def __init__(self, message: str = "Account is frozen or restricted", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="ACCOUNT_FROZEN", status_code=403, details=details)


class UnbalancedLedgerException(FinTechException):
    def __init__(self, message: str = "Financial ledger entry is unbalanced (Debits != Credits)", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="UNBALANCED_LEDGER", status_code=422, details=details)


class FraudBlockedException(FinTechException):
    def __init__(self, message: str = "Transaction blocked by real-time risk & fraud engine", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="FRAUD_BLOCKED", status_code=403, details=details)


class IdempotencyConflictException(FinTechException):
    def __init__(self, message: str = "Concurrent or duplicate request with same idempotency key", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="IDEMPOTENCY_CONFLICT", status_code=409, details=details)


class KYCRequiredException(FinTechException):
    def __init__(self, message: str = "Full KYC verification required to perform this action", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="KYC_REQUIRED", status_code=403, details=details)


class InvalidStateTransitionException(FinTechException):
    def __init__(self, message: str = "Invalid entity state transition requested", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="INVALID_STATE_TRANSITION", status_code=422, details=details)


class EntityNotFoundException(FinTechException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(message=f"{entity_name} with id {entity_id} not found", code="NOT_FOUND", status_code=404)
