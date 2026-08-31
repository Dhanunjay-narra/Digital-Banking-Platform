"""Role-Based Access Control (RBAC) System."""

from enum import Enum
from typing import Set, Dict
from finx_platform.security.permissions import Permission


class Role(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    BANK_ADMIN = "BANK_ADMIN"
    OPERATIONS_ADMIN = "OPERATIONS_ADMIN"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    FINANCE_OFFICER = "FINANCE_OFFICER"
    LOAN_OFFICER = "LOAN_OFFICER"
    RISK_ANALYST = "RISK_ANALYST"
    FRAUD_ANALYST = "FRAUD_ANALYST"
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER"
    MERCHANT_ADMIN = "MERCHANT_ADMIN"
    AUDITOR = "AUDITOR"
    REPORTING_USER = "REPORTING_USER"
    CUSTOMER = "CUSTOMER"


# Map each role to its exhaustive permissions
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.SUPER_ADMIN: set(Permission),  # All permissions

    Role.BANK_ADMIN: {
        Permission.AUTH_LOGIN, Permission.AUTH_MFA,
        Permission.CUSTOMER_READ_ALL, Permission.CUSTOMER_MANAGE,
        Permission.KYC_REVIEW, Permission.KYC_APPROVE, Permission.KYC_REJECT,
        Permission.ACCOUNT_CREATE, Permission.ACCOUNT_FREEZE, Permission.ACCOUNT_UNFREEZE, Permission.ACCOUNT_CLOSE,
        Permission.LEDGER_READ, Permission.LEDGER_POST, Permission.LEDGER_RECONCILE,
        Permission.TRANSACTION_VIEW_ALL, Permission.TRANSACTION_REVERSE,
        Permission.MERCHANT_MANAGE_ALL,
        Permission.LOAN_UNDERWRITE, Permission.LOAN_DISBURSE,
        Permission.CREDIT_DECISION,
        Permission.FRAUD_VIEW_ALERTS, Permission.COMPLIANCE_AML_VIEW,
        Permission.ADMIN_DASHBOARD_VIEW, Permission.ADMIN_AUDIT_VIEW, Permission.REPORTS_EXPORT
    },

    Role.OPERATIONS_ADMIN: {
        Permission.AUTH_LOGIN, Permission.CUSTOMER_READ_ALL,
        Permission.ACCOUNT_CREATE, Permission.ACCOUNT_FREEZE, Permission.ACCOUNT_UNFREEZE,
        Permission.TRANSACTION_VIEW_ALL, Permission.TRANSACTION_REVERSE,
        Permission.LEDGER_READ, Permission.LEDGER_RECONCILE,
        Permission.ADMIN_DASHBOARD_VIEW, Permission.REPORTS_EXPORT
    },

    Role.CUSTOMER_SUPPORT: {
        Permission.AUTH_LOGIN, Permission.CUSTOMER_READ_ALL,
        Permission.ACCOUNT_READ_SELF, Permission.TRANSACTION_VIEW_ALL,
        Permission.ADMIN_DASHBOARD_VIEW
    },

    Role.FINANCE_OFFICER: {
        Permission.AUTH_LOGIN, Permission.LEDGER_READ, Permission.LEDGER_POST, Permission.LEDGER_RECONCILE,
        Permission.TRANSACTION_VIEW_ALL, Permission.MERCHANT_SETTLEMENT,
        Permission.ADMIN_DASHBOARD_VIEW, Permission.REPORTS_EXPORT
    },

    Role.LOAN_OFFICER: {
        Permission.AUTH_LOGIN, Permission.CUSTOMER_READ_ALL,
        Permission.LOAN_UNDERWRITE, Permission.LOAN_DISBURSE,
        Permission.CREDIT_SCORE_VIEW, Permission.CREDIT_DECISION,
        Permission.ADMIN_DASHBOARD_VIEW, Permission.REPORTS_EXPORT
    },

    Role.RISK_ANALYST: {
        Permission.AUTH_LOGIN, Permission.FRAUD_VIEW_ALERTS, Permission.FRAUD_RESOLVE_CASE,
        Permission.TRANSACTION_VIEW_ALL, Permission.CREDIT_SCORE_VIEW,
        Permission.ADMIN_DASHBOARD_VIEW, Permission.REPORTS_EXPORT
    },

    Role.FRAUD_ANALYST: {
        Permission.AUTH_LOGIN, Permission.FRAUD_VIEW_ALERTS, Permission.FRAUD_RESOLVE_CASE,
        Permission.ACCOUNT_FREEZE, Permission.TRANSACTION_VIEW_ALL,
        Permission.ADMIN_DASHBOARD_VIEW, Permission.REPORTS_EXPORT
    },

    Role.COMPLIANCE_OFFICER: {
        Permission.AUTH_LOGIN, Permission.COMPLIANCE_AML_VIEW, Permission.COMPLIANCE_SAR_FILE,
        Permission.COMPLIANCE_SANCTIONS_CHECK, Permission.KYC_REVIEW, Permission.KYC_APPROVE,
        Permission.ADMIN_DASHBOARD_VIEW, Permission.ADMIN_AUDIT_VIEW, Permission.REPORTS_EXPORT
    },

    Role.MERCHANT_ADMIN: {
        Permission.AUTH_LOGIN, Permission.MERCHANT_CREATE_ORDER, Permission.MERCHANT_REFUND,
        Permission.MERCHANT_SETTLEMENT, Permission.REPORTS_EXPORT
    },

    Role.AUDITOR: {
        Permission.AUTH_LOGIN, Permission.ADMIN_AUDIT_VIEW, Permission.LEDGER_READ,
        Permission.TRANSACTION_VIEW_ALL, Permission.REPORTS_EXPORT, Permission.ADMIN_DASHBOARD_VIEW
    },

    Role.REPORTING_USER: {
        Permission.AUTH_LOGIN, Permission.REPORTS_EXPORT, Permission.ADMIN_DASHBOARD_VIEW
    },

    Role.CUSTOMER: {
        Permission.AUTH_LOGIN, Permission.AUTH_MFA,
        Permission.CUSTOMER_READ_SELF, Permission.CUSTOMER_UPDATE_SELF,
        Permission.KYC_SUBMIT,
        Permission.ACCOUNT_READ_SELF,
        Permission.TRANSACTION_INITIATE, Permission.TRANSACTION_AUTHORIZE,
        Permission.UPI_PAY, Permission.UPI_COLLECT,
        Permission.WALLET_TOPUP, Permission.WALLET_WITHDRAW, Permission.WALLET_TRANSFER,
        Permission.CARD_ISSUE, Permission.CARD_MANAGE_CONTROLS, Permission.CARD_SET_PIN, Permission.CARD_BLOCK,
        Permission.LOAN_APPLY, Permission.LOAN_REPAY, Permission.CREDIT_SCORE_VIEW,
        Permission.INVESTMENT_TRADE, Permission.INVESTMENT_MANAGE,
        Permission.INSURANCE_QUOTE, Permission.INSURANCE_BUY,
        Permission.REPORTS_EXPORT
    }
}


def has_permission(role: Role, permission: Permission) -> bool:
    role_perms = ROLE_PERMISSIONS.get(role, set())
    return permission in role_perms
