"""Comprehensive Double-Entry Ledger Posting Rules Matrix for Banking Operations."""

DOUBLE_ENTRY_POSTING_MATRIX = {
    "CASH_DEPOSIT_BRANCH": {
        "event_code": "CASH_DEPOSIT_BRANCH",
        "description": "Cash deposited at bank branch",
        "postings": [
            {"account_code": "1000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CASH_DEPOSIT_BRANCH_REVERSAL": {
        "event_code": "CASH_DEPOSIT_BRANCH_REVERSAL",
        "description": "Reversal of Cash deposited at bank branch",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CASH_DEPOSIT_BRANCH_RETRY": {
        "event_code": "CASH_DEPOSIT_BRANCH_RETRY",
        "description": "Cash deposited at bank branch (RETRY)",
        "postings": [
            {"account_code": "1000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CASH_DEPOSIT_BRANCH_ADJUSTMENT": {
        "event_code": "CASH_DEPOSIT_BRANCH_ADJUSTMENT",
        "description": "Cash deposited at bank branch (ADJUSTMENT)",
        "postings": [
            {"account_code": "1000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CASH_WITHDRAWAL_ATM": {
        "event_code": "CASH_WITHDRAWAL_ATM",
        "description": "Cash dispensed at ATM",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CASH_WITHDRAWAL_ATM_REVERSAL": {
        "event_code": "CASH_WITHDRAWAL_ATM_REVERSAL",
        "description": "Reversal of Cash dispensed at ATM",
        "postings": [
            {"account_code": "1000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CASH_WITHDRAWAL_ATM_RETRY": {
        "event_code": "CASH_WITHDRAWAL_ATM_RETRY",
        "description": "Cash dispensed at ATM (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CASH_WITHDRAWAL_ATM_ADJUSTMENT": {
        "event_code": "CASH_WITHDRAWAL_ATM_ADJUSTMENT",
        "description": "Cash dispensed at ATM (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_OUTBOUND_TRANSFER": {
        "event_code": "IMPS_OUTBOUND_TRANSFER",
        "description": "Outbound IMPS interbank transfer",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_OUTBOUND_TRANSFER_REVERSAL": {
        "event_code": "IMPS_OUTBOUND_TRANSFER_REVERSAL",
        "description": "Reversal of Outbound IMPS interbank transfer",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_OUTBOUND_TRANSFER_RETRY": {
        "event_code": "IMPS_OUTBOUND_TRANSFER_RETRY",
        "description": "Outbound IMPS interbank transfer (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_OUTBOUND_TRANSFER_ADJUSTMENT": {
        "event_code": "IMPS_OUTBOUND_TRANSFER_ADJUSTMENT",
        "description": "Outbound IMPS interbank transfer (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_INBOUND_TRANSFER": {
        "event_code": "IMPS_INBOUND_TRANSFER",
        "description": "Inbound IMPS transfer received",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_INBOUND_TRANSFER_REVERSAL": {
        "event_code": "IMPS_INBOUND_TRANSFER_REVERSAL",
        "description": "Reversal of Inbound IMPS transfer received",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_INBOUND_TRANSFER_RETRY": {
        "event_code": "IMPS_INBOUND_TRANSFER_RETRY",
        "description": "Inbound IMPS transfer received (RETRY)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "IMPS_INBOUND_TRANSFER_ADJUSTMENT": {
        "event_code": "IMPS_INBOUND_TRANSFER_ADJUSTMENT",
        "description": "Inbound IMPS transfer received (ADJUSTMENT)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_OUTBOUND_SETTLEMENT": {
        "event_code": "NEFT_OUTBOUND_SETTLEMENT",
        "description": "NEFT batch outbound settlement",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_OUTBOUND_SETTLEMENT_REVERSAL": {
        "event_code": "NEFT_OUTBOUND_SETTLEMENT_REVERSAL",
        "description": "Reversal of NEFT batch outbound settlement",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_OUTBOUND_SETTLEMENT_RETRY": {
        "event_code": "NEFT_OUTBOUND_SETTLEMENT_RETRY",
        "description": "NEFT batch outbound settlement (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_OUTBOUND_SETTLEMENT_ADJUSTMENT": {
        "event_code": "NEFT_OUTBOUND_SETTLEMENT_ADJUSTMENT",
        "description": "NEFT batch outbound settlement (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_INBOUND_SETTLEMENT": {
        "event_code": "NEFT_INBOUND_SETTLEMENT",
        "description": "NEFT inbound batch credit",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_INBOUND_SETTLEMENT_REVERSAL": {
        "event_code": "NEFT_INBOUND_SETTLEMENT_REVERSAL",
        "description": "Reversal of NEFT inbound batch credit",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_INBOUND_SETTLEMENT_RETRY": {
        "event_code": "NEFT_INBOUND_SETTLEMENT_RETRY",
        "description": "NEFT inbound batch credit (RETRY)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "NEFT_INBOUND_SETTLEMENT_ADJUSTMENT": {
        "event_code": "NEFT_INBOUND_SETTLEMENT_ADJUSTMENT",
        "description": "NEFT inbound batch credit (ADJUSTMENT)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_DEBIT": {
        "event_code": "UPI_P2P_DEBIT",
        "description": "UPI P2P transfer sent to external VPA",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_DEBIT_REVERSAL": {
        "event_code": "UPI_P2P_DEBIT_REVERSAL",
        "description": "Reversal of UPI P2P transfer sent to external VPA",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_DEBIT_RETRY": {
        "event_code": "UPI_P2P_DEBIT_RETRY",
        "description": "UPI P2P transfer sent to external VPA (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_DEBIT_ADJUSTMENT": {
        "event_code": "UPI_P2P_DEBIT_ADJUSTMENT",
        "description": "UPI P2P transfer sent to external VPA (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_CREDIT": {
        "event_code": "UPI_P2P_CREDIT",
        "description": "UPI P2P transfer received from external VPA",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_CREDIT_REVERSAL": {
        "event_code": "UPI_P2P_CREDIT_REVERSAL",
        "description": "Reversal of UPI P2P transfer received from external VPA",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_CREDIT_RETRY": {
        "event_code": "UPI_P2P_CREDIT_RETRY",
        "description": "UPI P2P transfer received from external VPA (RETRY)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2P_CREDIT_ADJUSTMENT": {
        "event_code": "UPI_P2P_CREDIT_ADJUSTMENT",
        "description": "UPI P2P transfer received from external VPA (ADJUSTMENT)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2M_MERCHANT_PURCHASE": {
        "event_code": "UPI_P2M_MERCHANT_PURCHASE",
        "description": "UPI merchant payment",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2M_MERCHANT_PURCHASE_REVERSAL": {
        "event_code": "UPI_P2M_MERCHANT_PURCHASE_REVERSAL",
        "description": "Reversal of UPI merchant payment",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2M_MERCHANT_PURCHASE_RETRY": {
        "event_code": "UPI_P2M_MERCHANT_PURCHASE_RETRY",
        "description": "UPI merchant payment (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UPI_P2M_MERCHANT_PURCHASE_ADJUSTMENT": {
        "event_code": "UPI_P2M_MERCHANT_PURCHASE_ADJUSTMENT",
        "description": "UPI merchant payment (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_TOPUP_VIA_BANK": {
        "event_code": "WALLET_TOPUP_VIA_BANK",
        "description": "Wallet load from linked savings account",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_TOPUP_VIA_BANK_REVERSAL": {
        "event_code": "WALLET_TOPUP_VIA_BANK_REVERSAL",
        "description": "Reversal of Wallet load from linked savings account",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_TOPUP_VIA_BANK_RETRY": {
        "event_code": "WALLET_TOPUP_VIA_BANK_RETRY",
        "description": "Wallet load from linked savings account (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_TOPUP_VIA_BANK_ADJUSTMENT": {
        "event_code": "WALLET_TOPUP_VIA_BANK_ADJUSTMENT",
        "description": "Wallet load from linked savings account (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_WITHDRAWAL_TO_BANK": {
        "event_code": "WALLET_WITHDRAWAL_TO_BANK",
        "description": "Wallet redemption to savings account",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_WITHDRAWAL_TO_BANK_REVERSAL": {
        "event_code": "WALLET_WITHDRAWAL_TO_BANK_REVERSAL",
        "description": "Reversal of Wallet redemption to savings account",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_WITHDRAWAL_TO_BANK_RETRY": {
        "event_code": "WALLET_WITHDRAWAL_TO_BANK_RETRY",
        "description": "Wallet redemption to savings account (RETRY)",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_WITHDRAWAL_TO_BANK_ADJUSTMENT": {
        "event_code": "WALLET_WITHDRAWAL_TO_BANK_ADJUSTMENT",
        "description": "Wallet redemption to savings account (ADJUSTMENT)",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_P2P_TRANSFER": {
        "event_code": "WALLET_P2P_TRANSFER",
        "description": "Wallet to wallet peer transfer",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_P2P_TRANSFER_REVERSAL": {
        "event_code": "WALLET_P2P_TRANSFER_REVERSAL",
        "description": "Reversal of Wallet to wallet peer transfer",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_P2P_TRANSFER_RETRY": {
        "event_code": "WALLET_P2P_TRANSFER_RETRY",
        "description": "Wallet to wallet peer transfer (RETRY)",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "WALLET_P2P_TRANSFER_ADJUSTMENT": {
        "event_code": "WALLET_P2P_TRANSFER_ADJUSTMENT",
        "description": "Wallet to wallet peer transfer (ADJUSTMENT)",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_POS_PURCHASE": {
        "event_code": "CARD_POS_PURCHASE",
        "description": "RuPay Card POS terminal transaction",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_POS_PURCHASE_REVERSAL": {
        "event_code": "CARD_POS_PURCHASE_REVERSAL",
        "description": "Reversal of RuPay Card POS terminal transaction",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_POS_PURCHASE_RETRY": {
        "event_code": "CARD_POS_PURCHASE_RETRY",
        "description": "RuPay Card POS terminal transaction (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_POS_PURCHASE_ADJUSTMENT": {
        "event_code": "CARD_POS_PURCHASE_ADJUSTMENT",
        "description": "RuPay Card POS terminal transaction (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ECOMMERCE_PAYMENT": {
        "event_code": "CARD_ECOMMERCE_PAYMENT",
        "description": "RuPay Card online e-commerce checkout",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ECOMMERCE_PAYMENT_REVERSAL": {
        "event_code": "CARD_ECOMMERCE_PAYMENT_REVERSAL",
        "description": "Reversal of RuPay Card online e-commerce checkout",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ECOMMERCE_PAYMENT_RETRY": {
        "event_code": "CARD_ECOMMERCE_PAYMENT_RETRY",
        "description": "RuPay Card online e-commerce checkout (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ECOMMERCE_PAYMENT_ADJUSTMENT": {
        "event_code": "CARD_ECOMMERCE_PAYMENT_ADJUSTMENT",
        "description": "RuPay Card online e-commerce checkout (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ATM_INTERCHANGE_FEE": {
        "event_code": "CARD_ATM_INTERCHANGE_FEE",
        "description": "Interbank ATM interchange fee expense",
        "postings": [
            {"account_code": "5000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ATM_INTERCHANGE_FEE_REVERSAL": {
        "event_code": "CARD_ATM_INTERCHANGE_FEE_REVERSAL",
        "description": "Reversal of Interbank ATM interchange fee expense",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "5000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ATM_INTERCHANGE_FEE_RETRY": {
        "event_code": "CARD_ATM_INTERCHANGE_FEE_RETRY",
        "description": "Interbank ATM interchange fee expense (RETRY)",
        "postings": [
            {"account_code": "5000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ATM_INTERCHANGE_FEE_ADJUSTMENT": {
        "event_code": "CARD_ATM_INTERCHANGE_FEE_ADJUSTMENT",
        "description": "Interbank ATM interchange fee expense (ADJUSTMENT)",
        "postings": [
            {"account_code": "5000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ANNUAL_MAINTENANCE_FEE": {
        "event_code": "CARD_ANNUAL_MAINTENANCE_FEE",
        "description": "Card annual membership fee collection",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ANNUAL_MAINTENANCE_FEE_REVERSAL": {
        "event_code": "CARD_ANNUAL_MAINTENANCE_FEE_REVERSAL",
        "description": "Reversal of Card annual membership fee collection",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ANNUAL_MAINTENANCE_FEE_RETRY": {
        "event_code": "CARD_ANNUAL_MAINTENANCE_FEE_RETRY",
        "description": "Card annual membership fee collection (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CARD_ANNUAL_MAINTENANCE_FEE_ADJUSTMENT": {
        "event_code": "CARD_ANNUAL_MAINTENANCE_FEE_ADJUSTMENT",
        "description": "Card annual membership fee collection (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_PERSONAL": {
        "event_code": "LOAN_DISBURSEMENT_PERSONAL",
        "description": "Personal loan disbursed to customer savings",
        "postings": [
            {"account_code": "1030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_PERSONAL_REVERSAL": {
        "event_code": "LOAN_DISBURSEMENT_PERSONAL_REVERSAL",
        "description": "Reversal of Personal loan disbursed to customer savings",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_PERSONAL_RETRY": {
        "event_code": "LOAN_DISBURSEMENT_PERSONAL_RETRY",
        "description": "Personal loan disbursed to customer savings (RETRY)",
        "postings": [
            {"account_code": "1030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_PERSONAL_ADJUSTMENT": {
        "event_code": "LOAN_DISBURSEMENT_PERSONAL_ADJUSTMENT",
        "description": "Personal loan disbursed to customer savings (ADJUSTMENT)",
        "postings": [
            {"account_code": "1030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_HOME": {
        "event_code": "LOAN_DISBURSEMENT_HOME",
        "description": "Home loan disbursed to builder current account",
        "postings": [
            {"account_code": "1030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_HOME_REVERSAL": {
        "event_code": "LOAN_DISBURSEMENT_HOME_REVERSAL",
        "description": "Reversal of Home loan disbursed to builder current account",
        "postings": [
            {"account_code": "2010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_HOME_RETRY": {
        "event_code": "LOAN_DISBURSEMENT_HOME_RETRY",
        "description": "Home loan disbursed to builder current account (RETRY)",
        "postings": [
            {"account_code": "1030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_DISBURSEMENT_HOME_ADJUSTMENT": {
        "event_code": "LOAN_DISBURSEMENT_HOME_ADJUSTMENT",
        "description": "Home loan disbursed to builder current account (ADJUSTMENT)",
        "postings": [
            {"account_code": "1030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_PRINCIPAL_REPAYMENT": {
        "event_code": "LOAN_EMI_PRINCIPAL_REPAYMENT",
        "description": "Loan monthly principal installment recovery",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_PRINCIPAL_REPAYMENT_REVERSAL": {
        "event_code": "LOAN_EMI_PRINCIPAL_REPAYMENT_REVERSAL",
        "description": "Reversal of Loan monthly principal installment recovery",
        "postings": [
            {"account_code": "1030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_PRINCIPAL_REPAYMENT_RETRY": {
        "event_code": "LOAN_EMI_PRINCIPAL_REPAYMENT_RETRY",
        "description": "Loan monthly principal installment recovery (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_PRINCIPAL_REPAYMENT_ADJUSTMENT": {
        "event_code": "LOAN_EMI_PRINCIPAL_REPAYMENT_ADJUSTMENT",
        "description": "Loan monthly principal installment recovery (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_INTEREST_REPAYMENT": {
        "event_code": "LOAN_EMI_INTEREST_REPAYMENT",
        "description": "Loan monthly interest recovery to revenue",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_INTEREST_REPAYMENT_REVERSAL": {
        "event_code": "LOAN_EMI_INTEREST_REPAYMENT_REVERSAL",
        "description": "Reversal of Loan monthly interest recovery to revenue",
        "postings": [
            {"account_code": "4010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_INTEREST_REPAYMENT_RETRY": {
        "event_code": "LOAN_EMI_INTEREST_REPAYMENT_RETRY",
        "description": "Loan monthly interest recovery to revenue (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_EMI_INTEREST_REPAYMENT_ADJUSTMENT": {
        "event_code": "LOAN_EMI_INTEREST_REPAYMENT_ADJUSTMENT",
        "description": "Loan monthly interest recovery to revenue (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_PROCESSING_FEE": {
        "event_code": "LOAN_PROCESSING_FEE",
        "description": "Upfront loan origination processing fee",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_PROCESSING_FEE_REVERSAL": {
        "event_code": "LOAN_PROCESSING_FEE_REVERSAL",
        "description": "Reversal of Upfront loan origination processing fee",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_PROCESSING_FEE_RETRY": {
        "event_code": "LOAN_PROCESSING_FEE_RETRY",
        "description": "Upfront loan origination processing fee (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_PROCESSING_FEE_ADJUSTMENT": {
        "event_code": "LOAN_PROCESSING_FEE_ADJUSTMENT",
        "description": "Upfront loan origination processing fee (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_LATE_PAYMENT_PENALTY": {
        "event_code": "LOAN_LATE_PAYMENT_PENALTY",
        "description": "Overdue EMI late penalty recovery",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_LATE_PAYMENT_PENALTY_REVERSAL": {
        "event_code": "LOAN_LATE_PAYMENT_PENALTY_REVERSAL",
        "description": "Reversal of Overdue EMI late penalty recovery",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_LATE_PAYMENT_PENALTY_RETRY": {
        "event_code": "LOAN_LATE_PAYMENT_PENALTY_RETRY",
        "description": "Overdue EMI late penalty recovery (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "LOAN_LATE_PAYMENT_PENALTY_ADJUSTMENT": {
        "event_code": "LOAN_LATE_PAYMENT_PENALTY_ADJUSTMENT",
        "description": "Overdue EMI late penalty recovery (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "SAVINGS_INTEREST_CAPITALIZATION": {
        "event_code": "SAVINGS_INTEREST_CAPITALIZATION",
        "description": "Quarterly interest credited to customer savings",
        "postings": [
            {"account_code": "5010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "SAVINGS_INTEREST_CAPITALIZATION_REVERSAL": {
        "event_code": "SAVINGS_INTEREST_CAPITALIZATION_REVERSAL",
        "description": "Reversal of Quarterly interest credited to customer savings",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "5010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "SAVINGS_INTEREST_CAPITALIZATION_RETRY": {
        "event_code": "SAVINGS_INTEREST_CAPITALIZATION_RETRY",
        "description": "Quarterly interest credited to customer savings (RETRY)",
        "postings": [
            {"account_code": "5010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "SAVINGS_INTEREST_CAPITALIZATION_ADJUSTMENT": {
        "event_code": "SAVINGS_INTEREST_CAPITALIZATION_ADJUSTMENT",
        "description": "Quarterly interest credited to customer savings (ADJUSTMENT)",
        "postings": [
            {"account_code": "5010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "AMB_SHORTFALL_PENALTY": {
        "event_code": "AMB_SHORTFALL_PENALTY",
        "description": "Average monthly balance deficit charge",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "AMB_SHORTFALL_PENALTY_REVERSAL": {
        "event_code": "AMB_SHORTFALL_PENALTY_REVERSAL",
        "description": "Reversal of Average monthly balance deficit charge",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "AMB_SHORTFALL_PENALTY_RETRY": {
        "event_code": "AMB_SHORTFALL_PENALTY_RETRY",
        "description": "Average monthly balance deficit charge (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "AMB_SHORTFALL_PENALTY_ADJUSTMENT": {
        "event_code": "AMB_SHORTFALL_PENALTY_ADJUSTMENT",
        "description": "Average monthly balance deficit charge (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHEQUE_BOUNCE_PENALTY": {
        "event_code": "CHEQUE_BOUNCE_PENALTY",
        "description": "Inward cheque dishonour charge",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHEQUE_BOUNCE_PENALTY_REVERSAL": {
        "event_code": "CHEQUE_BOUNCE_PENALTY_REVERSAL",
        "description": "Reversal of Inward cheque dishonour charge",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHEQUE_BOUNCE_PENALTY_RETRY": {
        "event_code": "CHEQUE_BOUNCE_PENALTY_RETRY",
        "description": "Inward cheque dishonour charge (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHEQUE_BOUNCE_PENALTY_ADJUSTMENT": {
        "event_code": "CHEQUE_BOUNCE_PENALTY_ADJUSTMENT",
        "description": "Inward cheque dishonour charge (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_MDR_FEE_CAPTURE": {
        "event_code": "MERCHANT_MDR_FEE_CAPTURE",
        "description": "Merchant discount rate revenue retention",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_MDR_FEE_CAPTURE_REVERSAL": {
        "event_code": "MERCHANT_MDR_FEE_CAPTURE_REVERSAL",
        "description": "Reversal of Merchant discount rate revenue retention",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_MDR_FEE_CAPTURE_RETRY": {
        "event_code": "MERCHANT_MDR_FEE_CAPTURE_RETRY",
        "description": "Merchant discount rate revenue retention (RETRY)",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_MDR_FEE_CAPTURE_ADJUSTMENT": {
        "event_code": "MERCHANT_MDR_FEE_CAPTURE_ADJUSTMENT",
        "description": "Merchant discount rate revenue retention (ADJUSTMENT)",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_SETTLEMENT_PAYOUT": {
        "event_code": "MERCHANT_SETTLEMENT_PAYOUT",
        "description": "T+0 settlement credit to merchant bank account",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_SETTLEMENT_PAYOUT_REVERSAL": {
        "event_code": "MERCHANT_SETTLEMENT_PAYOUT_REVERSAL",
        "description": "Reversal of T+0 settlement credit to merchant bank account",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_SETTLEMENT_PAYOUT_RETRY": {
        "event_code": "MERCHANT_SETTLEMENT_PAYOUT_RETRY",
        "description": "T+0 settlement credit to merchant bank account (RETRY)",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_SETTLEMENT_PAYOUT_ADJUSTMENT": {
        "event_code": "MERCHANT_SETTLEMENT_PAYOUT_ADJUSTMENT",
        "description": "T+0 settlement credit to merchant bank account (ADJUSTMENT)",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_DISPUTE_HOLD": {
        "event_code": "MERCHANT_DISPUTE_HOLD",
        "description": "Merchant balance held pending chargeback review",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2090", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_DISPUTE_HOLD_REVERSAL": {
        "event_code": "MERCHANT_DISPUTE_HOLD_REVERSAL",
        "description": "Reversal of Merchant balance held pending chargeback review",
        "postings": [
            {"account_code": "2090", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_DISPUTE_HOLD_RETRY": {
        "event_code": "MERCHANT_DISPUTE_HOLD_RETRY",
        "description": "Merchant balance held pending chargeback review (RETRY)",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2090", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "MERCHANT_DISPUTE_HOLD_ADJUSTMENT": {
        "event_code": "MERCHANT_DISPUTE_HOLD_ADJUSTMENT",
        "description": "Merchant balance held pending chargeback review (ADJUSTMENT)",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2090", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_CUSTOMER_REFUND": {
        "event_code": "CHARGEBACK_CUSTOMER_REFUND",
        "description": "Dispute won - chargeback refunded to customer",
        "postings": [
            {"account_code": "2090", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_CUSTOMER_REFUND_REVERSAL": {
        "event_code": "CHARGEBACK_CUSTOMER_REFUND_REVERSAL",
        "description": "Reversal of Dispute won - chargeback refunded to customer",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2090", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_CUSTOMER_REFUND_RETRY": {
        "event_code": "CHARGEBACK_CUSTOMER_REFUND_RETRY",
        "description": "Dispute won - chargeback refunded to customer (RETRY)",
        "postings": [
            {"account_code": "2090", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_CUSTOMER_REFUND_ADJUSTMENT": {
        "event_code": "CHARGEBACK_CUSTOMER_REFUND_ADJUSTMENT",
        "description": "Dispute won - chargeback refunded to customer (ADJUSTMENT)",
        "postings": [
            {"account_code": "2090", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_MERCHANT_RELEASE": {
        "event_code": "CHARGEBACK_MERCHANT_RELEASE",
        "description": "Dispute won by merchant - hold released",
        "postings": [
            {"account_code": "2090", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_MERCHANT_RELEASE_REVERSAL": {
        "event_code": "CHARGEBACK_MERCHANT_RELEASE_REVERSAL",
        "description": "Reversal of Dispute won by merchant - hold released",
        "postings": [
            {"account_code": "2030", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2090", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_MERCHANT_RELEASE_RETRY": {
        "event_code": "CHARGEBACK_MERCHANT_RELEASE_RETRY",
        "description": "Dispute won by merchant - hold released (RETRY)",
        "postings": [
            {"account_code": "2090", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "CHARGEBACK_MERCHANT_RELEASE_ADJUSTMENT": {
        "event_code": "CHARGEBACK_MERCHANT_RELEASE_ADJUSTMENT",
        "description": "Dispute won by merchant - hold released (ADJUSTMENT)",
        "postings": [
            {"account_code": "2090", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2030", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_BUY": {
        "event_code": "INVESTMENT_MUTUAL_FUND_BUY",
        "description": "Mutual fund subscription payment to AMC",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_BUY_REVERSAL": {
        "event_code": "INVESTMENT_MUTUAL_FUND_BUY_REVERSAL",
        "description": "Reversal of Mutual fund subscription payment to AMC",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_BUY_RETRY": {
        "event_code": "INVESTMENT_MUTUAL_FUND_BUY_RETRY",
        "description": "Mutual fund subscription payment to AMC (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_BUY_ADJUSTMENT": {
        "event_code": "INVESTMENT_MUTUAL_FUND_BUY_ADJUSTMENT",
        "description": "Mutual fund subscription payment to AMC (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_REDEEM": {
        "event_code": "INVESTMENT_MUTUAL_FUND_REDEEM",
        "description": "Mutual fund redemption proceeds credited",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_REDEEM_REVERSAL": {
        "event_code": "INVESTMENT_MUTUAL_FUND_REDEEM_REVERSAL",
        "description": "Reversal of Mutual fund redemption proceeds credited",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_REDEEM_RETRY": {
        "event_code": "INVESTMENT_MUTUAL_FUND_REDEEM_RETRY",
        "description": "Mutual fund redemption proceeds credited (RETRY)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_MUTUAL_FUND_REDEEM_ADJUSTMENT": {
        "event_code": "INVESTMENT_MUTUAL_FUND_REDEEM_ADJUSTMENT",
        "description": "Mutual fund redemption proceeds credited (ADJUSTMENT)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_SIP_AUTODEBIT": {
        "event_code": "INVESTMENT_SIP_AUTODEBIT",
        "description": "SIP monthly automated investment debit",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_SIP_AUTODEBIT_REVERSAL": {
        "event_code": "INVESTMENT_SIP_AUTODEBIT_REVERSAL",
        "description": "Reversal of SIP monthly automated investment debit",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_SIP_AUTODEBIT_RETRY": {
        "event_code": "INVESTMENT_SIP_AUTODEBIT_RETRY",
        "description": "SIP monthly automated investment debit (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_SIP_AUTODEBIT_ADJUSTMENT": {
        "event_code": "INVESTMENT_SIP_AUTODEBIT_ADJUSTMENT",
        "description": "SIP monthly automated investment debit (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_GOLD_VAULT_BUY": {
        "event_code": "INVESTMENT_GOLD_VAULT_BUY",
        "description": "Digital 24K gold purchase debit",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_GOLD_VAULT_BUY_REVERSAL": {
        "event_code": "INVESTMENT_GOLD_VAULT_BUY_REVERSAL",
        "description": "Reversal of Digital 24K gold purchase debit",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_GOLD_VAULT_BUY_RETRY": {
        "event_code": "INVESTMENT_GOLD_VAULT_BUY_RETRY",
        "description": "Digital 24K gold purchase debit (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INVESTMENT_GOLD_VAULT_BUY_ADJUSTMENT": {
        "event_code": "INVESTMENT_GOLD_VAULT_BUY_ADJUSTMENT",
        "description": "Digital 24K gold purchase debit (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_PREMIUM_COLLECTION": {
        "event_code": "INSURANCE_PREMIUM_COLLECTION",
        "description": "Health/Life insurance premium payment to insurer",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_PREMIUM_COLLECTION_REVERSAL": {
        "event_code": "INSURANCE_PREMIUM_COLLECTION_REVERSAL",
        "description": "Reversal of Health/Life insurance premium payment to insurer",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_PREMIUM_COLLECTION_RETRY": {
        "event_code": "INSURANCE_PREMIUM_COLLECTION_RETRY",
        "description": "Health/Life insurance premium payment to insurer (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_PREMIUM_COLLECTION_ADJUSTMENT": {
        "event_code": "INSURANCE_PREMIUM_COLLECTION_ADJUSTMENT",
        "description": "Health/Life insurance premium payment to insurer (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_CLAIM_DISBURSEMENT": {
        "event_code": "INSURANCE_CLAIM_DISBURSEMENT",
        "description": "Insurance claim settlement credit to customer",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_CLAIM_DISBURSEMENT_REVERSAL": {
        "event_code": "INSURANCE_CLAIM_DISBURSEMENT_REVERSAL",
        "description": "Reversal of Insurance claim settlement credit to customer",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_CLAIM_DISBURSEMENT_RETRY": {
        "event_code": "INSURANCE_CLAIM_DISBURSEMENT_RETRY",
        "description": "Insurance claim settlement credit to customer (RETRY)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "INSURANCE_CLAIM_DISBURSEMENT_ADJUSTMENT": {
        "event_code": "INSURANCE_CLAIM_DISBURSEMENT_ADJUSTMENT",
        "description": "Insurance claim settlement credit to customer (ADJUSTMENT)",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UTILITY_BILL_PAYMENT_BBPS": {
        "event_code": "UTILITY_BILL_PAYMENT_BBPS",
        "description": "Electricity/Water bill paid via BBPS rail",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UTILITY_BILL_PAYMENT_BBPS_REVERSAL": {
        "event_code": "UTILITY_BILL_PAYMENT_BBPS_REVERSAL",
        "description": "Reversal of Electricity/Water bill paid via BBPS rail",
        "postings": [
            {"account_code": "1010", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UTILITY_BILL_PAYMENT_BBPS_RETRY": {
        "event_code": "UTILITY_BILL_PAYMENT_BBPS_RETRY",
        "description": "Electricity/Water bill paid via BBPS rail (RETRY)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "UTILITY_BILL_PAYMENT_BBPS_ADJUSTMENT": {
        "event_code": "UTILITY_BILL_PAYMENT_BBPS_ADJUSTMENT",
        "description": "Electricity/Water bill paid via BBPS rail (ADJUSTMENT)",
        "postings": [
            {"account_code": "2000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1010", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_COLLECTION_ON_FEES": {
        "event_code": "TAX_GST_COLLECTION_ON_FEES",
        "description": "18% GST collected on fee transferred to tax liability",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2080", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_COLLECTION_ON_FEES_REVERSAL": {
        "event_code": "TAX_GST_COLLECTION_ON_FEES_REVERSAL",
        "description": "Reversal of 18% GST collected on fee transferred to tax liability",
        "postings": [
            {"account_code": "2080", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "4000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_COLLECTION_ON_FEES_RETRY": {
        "event_code": "TAX_GST_COLLECTION_ON_FEES_RETRY",
        "description": "18% GST collected on fee transferred to tax liability (RETRY)",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2080", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_COLLECTION_ON_FEES_ADJUSTMENT": {
        "event_code": "TAX_GST_COLLECTION_ON_FEES_ADJUSTMENT",
        "description": "18% GST collected on fee transferred to tax liability (ADJUSTMENT)",
        "postings": [
            {"account_code": "4000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2080", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_REMITTANCE_GOVERNMENT": {
        "event_code": "TAX_GST_REMITTANCE_GOVERNMENT",
        "description": "GST tax remittance paid to central treasury",
        "postings": [
            {"account_code": "2080", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_REMITTANCE_GOVERNMENT_REVERSAL": {
        "event_code": "TAX_GST_REMITTANCE_GOVERNMENT_REVERSAL",
        "description": "Reversal of GST tax remittance paid to central treasury",
        "postings": [
            {"account_code": "1000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2080", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_REMITTANCE_GOVERNMENT_RETRY": {
        "event_code": "TAX_GST_REMITTANCE_GOVERNMENT_RETRY",
        "description": "GST tax remittance paid to central treasury (RETRY)",
        "postings": [
            {"account_code": "2080", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "TAX_GST_REMITTANCE_GOVERNMENT_ADJUSTMENT": {
        "event_code": "TAX_GST_REMITTANCE_GOVERNMENT_ADJUSTMENT",
        "description": "GST tax remittance paid to central treasury (ADJUSTMENT)",
        "postings": [
            {"account_code": "2080", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "1000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "REWARDS_CASHBACK_ISSUANCE": {
        "event_code": "REWARDS_CASHBACK_ISSUANCE",
        "description": "Promotional cashback credited to customer wallet",
        "postings": [
            {"account_code": "5000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "REWARDS_CASHBACK_ISSUANCE_REVERSAL": {
        "event_code": "REWARDS_CASHBACK_ISSUANCE_REVERSAL",
        "description": "Reversal of Promotional cashback credited to customer wallet",
        "postings": [
            {"account_code": "2020", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "5000", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "REWARDS_CASHBACK_ISSUANCE_RETRY": {
        "event_code": "REWARDS_CASHBACK_ISSUANCE_RETRY",
        "description": "Promotional cashback credited to customer wallet (RETRY)",
        "postings": [
            {"account_code": "5000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
    "REWARDS_CASHBACK_ISSUANCE_ADJUSTMENT": {
        "event_code": "REWARDS_CASHBACK_ISSUANCE_ADJUSTMENT",
        "description": "Promotional cashback credited to customer wallet (ADJUSTMENT)",
        "postings": [
            {"account_code": "5000", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"},
            {"account_code": "2020", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"},
        ]
    },
}

def get_posting_rule(event_code: str):
    return DOUBLE_ENTRY_POSTING_MATRIX.get(event_code)
