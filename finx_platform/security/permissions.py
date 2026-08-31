"""Granular Financial & Platform Permissions."""

from enum import Enum


class Permission(str, Enum):
    # Customer & Auth
    AUTH_LOGIN = "auth:login"
    AUTH_MFA = "auth:mfa"
    CUSTOMER_READ_SELF = "customer:read_self"
    CUSTOMER_UPDATE_SELF = "customer:update_self"
    CUSTOMER_READ_ALL = "customer:read_all"
    CUSTOMER_MANAGE = "customer:manage"

    # KYC & Verification
    KYC_SUBMIT = "kyc:submit"
    KYC_REVIEW = "kyc:review"
    KYC_APPROVE = "kyc:approve"
    KYC_REJECT = "kyc:reject"

    # Accounts & Ledger
    ACCOUNT_READ_SELF = "account:read_self"
    ACCOUNT_CREATE = "account:create"
    ACCOUNT_FREEZE = "account:freeze"
    ACCOUNT_UNFREEZE = "account:unfreeze"
    ACCOUNT_CLOSE = "account:close"
    LEDGER_READ = "ledger:read"
    LEDGER_POST = "ledger:post"
    LEDGER_RECONCILE = "ledger:reconcile"

    # Transactions & Payments
    TRANSACTION_INITIATE = "transaction:initiate"
    TRANSACTION_AUTHORIZE = "transaction:authorize"
    TRANSACTION_REVERSE = "transaction:reverse"
    TRANSACTION_VIEW_ALL = "transaction:view_all"
    UPI_PAY = "upi:pay"
    UPI_COLLECT = "upi:collect"
    WALLET_TOPUP = "wallet:topup"
    WALLET_WITHDRAW = "wallet:withdraw"
    WALLET_TRANSFER = "wallet:transfer"

    # Cards
    CARD_ISSUE = "card:issue"
    CARD_MANAGE_CONTROLS = "card:manage_controls"
    CARD_SET_PIN = "card:set_pin"
    CARD_BLOCK = "card:block"

    # Merchants & Gateway
    MERCHANT_CREATE_ORDER = "merchant:create_order"
    MERCHANT_REFUND = "merchant:refund"
    MERCHANT_SETTLEMENT = "merchant:settlement"
    MERCHANT_MANAGE_ALL = "merchant:manage_all"

    # Loans & Credit
    LOAN_APPLY = "loan:apply"
    LOAN_UNDERWRITE = "loan:underwrite"
    LOAN_DISBURSE = "loan:disburse"
    LOAN_REPAY = "loan:repay"
    CREDIT_SCORE_VIEW = "credit:score_view"
    CREDIT_DECISION = "credit:decision"

    # Investments & Insurance
    INVESTMENT_TRADE = "investment:trade"
    INVESTMENT_MANAGE = "investment:manage"
    INSURANCE_QUOTE = "insurance:quote"
    INSURANCE_BUY = "insurance:buy"
    INSURANCE_CLAIM_MANAGE = "insurance:claim_manage"

    # Risk & Compliance
    FRAUD_VIEW_ALERTS = "fraud:view_alerts"
    FRAUD_RESOLVE_CASE = "fraud:resolve_case"
    COMPLIANCE_AML_VIEW = "compliance:aml_view"
    COMPLIANCE_SAR_FILE = "compliance:sar_file"
    COMPLIANCE_SANCTIONS_CHECK = "compliance:sanctions_check"

    # Admin & Audit
    ADMIN_CONFIG_MANAGE = "admin:config_manage"
    ADMIN_USER_MANAGE = "admin:user_manage"
    ADMIN_AUDIT_VIEW = "admin:audit_view"
    ADMIN_DASHBOARD_VIEW = "admin:dashboard_view"
    REPORTS_EXPORT = "reports:export"
