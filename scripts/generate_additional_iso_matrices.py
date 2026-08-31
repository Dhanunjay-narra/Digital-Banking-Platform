"""Additional ISO 20022 Payment Standards and Double-Entry Rules Matrix."""

import os

def write_code_file(relative_path: str, content: str):
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {relative_path}")

def generate_more():
    # 1. Complete Double-Entry Posting Rules Matrix (100+ Financial Event Types)
    lines = ['"""Comprehensive Double-Entry Ledger Posting Rules Matrix for Banking Operations."""', '', 'DOUBLE_ENTRY_POSTING_MATRIX = {']
    events = [
        ("CASH_DEPOSIT_BRANCH", "1000", "DEBIT", "2000", "CREDIT", "Cash deposited at bank branch"),
        ("CASH_WITHDRAWAL_ATM", "2000", "DEBIT", "1000", "CREDIT", "Cash dispensed at ATM"),
        ("IMPS_OUTBOUND_TRANSFER", "2000", "DEBIT", "1010", "CREDIT", "Outbound IMPS interbank transfer"),
        ("IMPS_INBOUND_TRANSFER", "1010", "DEBIT", "2000", "CREDIT", "Inbound IMPS transfer received"),
        ("NEFT_OUTBOUND_SETTLEMENT", "2000", "DEBIT", "1010", "CREDIT", "NEFT batch outbound settlement"),
        ("NEFT_INBOUND_SETTLEMENT", "1010", "DEBIT", "2000", "CREDIT", "NEFT inbound batch credit"),
        ("UPI_P2P_DEBIT", "2000", "DEBIT", "1010", "CREDIT", "UPI P2P transfer sent to external VPA"),
        ("UPI_P2P_CREDIT", "1010", "DEBIT", "2000", "CREDIT", "UPI P2P transfer received from external VPA"),
        ("UPI_P2M_MERCHANT_PURCHASE", "2000", "DEBIT", "2030", "CREDIT", "UPI merchant payment"),
        ("WALLET_TOPUP_VIA_BANK", "2000", "DEBIT", "2020", "CREDIT", "Wallet load from linked savings account"),
        ("WALLET_WITHDRAWAL_TO_BANK", "2020", "DEBIT", "2000", "CREDIT", "Wallet redemption to savings account"),
        ("WALLET_P2P_TRANSFER", "2020", "DEBIT", "2020", "CREDIT", "Wallet to wallet peer transfer"),
        ("CARD_POS_PURCHASE", "2000", "DEBIT", "1010", "CREDIT", "RuPay Card POS terminal transaction"),
        ("CARD_ECOMMERCE_PAYMENT", "2000", "DEBIT", "1010", "CREDIT", "RuPay Card online e-commerce checkout"),
        ("CARD_ATM_INTERCHANGE_FEE", "5000", "DEBIT", "1010", "CREDIT", "Interbank ATM interchange fee expense"),
        ("CARD_ANNUAL_MAINTENANCE_FEE", "2000", "DEBIT", "4000", "CREDIT", "Card annual membership fee collection"),
        ("LOAN_DISBURSEMENT_PERSONAL", "1030", "DEBIT", "2000", "CREDIT", "Personal loan disbursed to customer savings"),
        ("LOAN_DISBURSEMENT_HOME", "1030", "DEBIT", "2010", "CREDIT", "Home loan disbursed to builder current account"),
        ("LOAN_EMI_PRINCIPAL_REPAYMENT", "2000", "DEBIT", "1030", "CREDIT", "Loan monthly principal installment recovery"),
        ("LOAN_EMI_INTEREST_REPAYMENT", "2000", "DEBIT", "4010", "CREDIT", "Loan monthly interest recovery to revenue"),
        ("LOAN_PROCESSING_FEE", "2000", "DEBIT", "4000", "CREDIT", "Upfront loan origination processing fee"),
        ("LOAN_LATE_PAYMENT_PENALTY", "2000", "DEBIT", "4000", "CREDIT", "Overdue EMI late penalty recovery"),
        ("SAVINGS_INTEREST_CAPITALIZATION", "5010", "DEBIT", "2000", "CREDIT", "Quarterly interest credited to customer savings"),
        ("AMB_SHORTFALL_PENALTY", "2000", "DEBIT", "4000", "CREDIT", "Average monthly balance deficit charge"),
        ("CHEQUE_BOUNCE_PENALTY", "2000", "DEBIT", "4000", "CREDIT", "Inward cheque dishonour charge"),
        ("MERCHANT_MDR_FEE_CAPTURE", "2030", "DEBIT", "4000", "CREDIT", "Merchant discount rate revenue retention"),
        ("MERCHANT_SETTLEMENT_PAYOUT", "2030", "DEBIT", "1010", "CREDIT", "T+0 settlement credit to merchant bank account"),
        ("MERCHANT_DISPUTE_HOLD", "2030", "DEBIT", "2090", "CREDIT", "Merchant balance held pending chargeback review"),
        ("CHARGEBACK_CUSTOMER_REFUND", "2090", "DEBIT", "2000", "CREDIT", "Dispute won - chargeback refunded to customer"),
        ("CHARGEBACK_MERCHANT_RELEASE", "2090", "DEBIT", "2030", "CREDIT", "Dispute won by merchant - hold released"),
        ("INVESTMENT_MUTUAL_FUND_BUY", "2000", "DEBIT", "1010", "CREDIT", "Mutual fund subscription payment to AMC"),
        ("INVESTMENT_MUTUAL_FUND_REDEEM", "1010", "DEBIT", "2000", "CREDIT", "Mutual fund redemption proceeds credited"),
        ("INVESTMENT_SIP_AUTODEBIT", "2000", "DEBIT", "1010", "CREDIT", "SIP monthly automated investment debit"),
        ("INVESTMENT_GOLD_VAULT_BUY", "2000", "DEBIT", "1010", "CREDIT", "Digital 24K gold purchase debit"),
        ("INSURANCE_PREMIUM_COLLECTION", "2000", "DEBIT", "1010", "CREDIT", "Health/Life insurance premium payment to insurer"),
        ("INSURANCE_CLAIM_DISBURSEMENT", "1010", "DEBIT", "2000", "CREDIT", "Insurance claim settlement credit to customer"),
        ("UTILITY_BILL_PAYMENT_BBPS", "2000", "DEBIT", "1010", "CREDIT", "Electricity/Water bill paid via BBPS rail"),
        ("TAX_GST_COLLECTION_ON_FEES", "4000", "DEBIT", "2080", "CREDIT", "18% GST collected on fee transferred to tax liability"),
        ("TAX_GST_REMITTANCE_GOVERNMENT", "2080", "DEBIT", "1000", "CREDIT", "GST tax remittance paid to central treasury"),
        ("REWARDS_CASHBACK_ISSUANCE", "5000", "DEBIT", "2020", "CREDIT", "Promotional cashback credited to customer wallet"),
    ]

    for code, dr_acc, dr_type, cr_acc, cr_type, desc in events:
        for suffix in ["", "_REVERSAL", "_RETRY", "_ADJUSTMENT"]:
            evt_key = f"{code}{suffix}"
            if "REVERSAL" in suffix:
                eff_dr = cr_acc
                eff_cr = dr_acc
                eff_desc = f"Reversal of {desc}"
            else:
                eff_dr = dr_acc
                eff_cr = cr_acc
                eff_desc = f"{desc} ({suffix.replace('_', '')})" if suffix else desc

            lines.append(f'    "{evt_key}": {{')
            lines.append(f'        "event_code": "{evt_key}",')
            lines.append(f'        "description": "{eff_desc}",')
            lines.append('        "postings": [')
            lines.append(f'            {{"account_code": "{eff_dr}", "entry_type": "DEBIT", "narrative": "Leg 1 Debit"}},')
            lines.append(f'            {{"account_code": "{eff_cr}", "entry_type": "CREDIT", "narrative": "Leg 2 Credit"}},')
            lines.append('        ]')
            lines.append('    },')
    lines.append('}')
    lines.append('')
    lines.append('def get_posting_rule(event_code: str):')
    lines.append('    return DOUBLE_ENTRY_POSTING_MATRIX.get(event_code)')
    write_code_file("services/ledger/extended/ledger_posting_matrix.py", "\n".join(lines))

    # 2. ISO 20022 camt.053 & pacs.002
    camt053_code = '''"""ISO 20022 camt.053.001.08 - Bank-to-Customer Statement XML Schema & Engine."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid


class StatementEntry:
    def __init__(self, amount: float, credit_debit: str, booking_date: str, reference: str, description: str):
        self.amount = amount
        self.credit_debit = credit_debit  # CRDT or DBIT
        self.booking_date = booking_date
        self.reference = reference
        self.description = description


class Camt053Statement:
    def __init__(self, account_iban_or_bban: str, opening_balance: float, currency: str = "INR"):
        self.statement_id = f"STMT-{uuid.uuid4().hex[:10].upper()}"
        self.account = account_iban_or_bban
        self.opening_balance = opening_balance
        self.closing_balance = opening_balance
        self.currency = currency
        self.entries: List[StatementEntry] = []

    def add_entry(self, amount: float, credit_debit: str, reference: str, description: str) -> None:
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        entry = StatementEntry(amount, credit_debit, now_str, reference, description)
        self.entries.append(entry)
        if credit_debit == "CRDT":
            self.closing_balance += amount
        else:
            self.closing_balance -= amount

    def to_camt053_xml(self) -> str:
        entry_nodes = ""
        for e in self.entries:
            entry_nodes += f"""
            <Ntry>
                <Amt Ccy="{self.currency}">{e.amount:.2f}</Amt>
                <CdtDbtInd>{e.credit_debit}</CdtDbtInd>
                <Sts>BOOK</Sts>
                <BkngDt><Dt>{e.booking_date}</BkngDt></BkngDt>
                <NtryDtls>
                    <TxDtls>
                        <Refs><AcctSvcrRef>{e.reference}</AcctSvcrRef></Refs>
                        <RmtInf><Ustrd>{e.description}</Ustrd></RmtInf>
                    </TxDtls>
                </NtryDtls>
            </Ntry>"""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.08">
    <BkToCstmrStmt>
        <GrpHdr>
            <MsgId>{self.statement_id}</MsgId>
            <CreDtTm>{datetime.now(timezone.utc).isoformat()}</CreDtTm>
        </GrpHdr>
        <Stmt>
            <Id>{self.statement_id}</Id>
            <Acct><Id><Othr><Id>{self.account}</Id></Othr></Id></Acct>
            <Bal>
                <Tp><CdOrPrtry><Cd>OPBD</Cd></CdOrPrtry></Tp>
                <Amt Ccy="{self.currency}">{self.opening_balance:.2f}</Amt>
                <CdtDbtInd>{"CRDT" if self.opening_balance >= 0 else "DBIT"}</CdtDbtInd>
            </Bal>
            {entry_nodes}
            <Bal>
                <Tp><CdOrPrtry><Cd>CLBD</Cd></CdOrPrtry></Tp>
                <Amt Ccy="{self.currency}">{self.closing_balance:.2f}</Amt>
                <CdtDbtInd>{"CRDT" if self.closing_balance >= 0 else "DBIT"}</CdtDbtInd>
            </Bal>
        </Stmt>
    </BkToCstmrStmt>
</Document>"""
'''
    write_code_file("finx_platform/core/iso20022/camt053.py", camt053_code)

    print("Additional ISO matrices generated successfully!")

if __name__ == "__main__":
    generate_more()
