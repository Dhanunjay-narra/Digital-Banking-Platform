"""ISO 20022 camt.053.001.08 - Bank-to-Customer Statement XML Schema & Engine."""

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
