"""Financial Reporting & Statement Generation Engine."""

import csv
import io
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from services.transactions.models import FinancialTransaction
from services.accounts.models import BankAccount


class ReportingEngine:
    @staticmethod
    def generate_account_statement(db: Session, account_number: str, format_type: str = "json") -> Any:
        txs = db.query(FinancialTransaction).filter(
            (FinancialTransaction.source_account == account_number) | (FinancialTransaction.destination_account == account_number)
        ).order_by(FinancialTransaction.created_at.desc()).all()

        if format_type.lower() == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Transaction Reference", "Date", "Source", "Destination", "Type", "Amount", "Currency", "Status", "Description"])
            for t in txs:
                writer.writerow([
                    t.transaction_reference,
                    t.created_at.isoformat() if t.created_at else "",
                    t.source_account,
                    t.destination_account,
                    t.transaction_type,
                    t.amount,
                    t.currency,
                    t.status,
                    t.description
                ])
            return output.getvalue()

        return {
            "account_number": account_number,
            "statement_period": "Current Financial Year",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_transactions": len(txs),
            "transactions": [
                {
                    "reference": t.transaction_reference,
                    "date": t.created_at.isoformat() if t.created_at else "",
                    "type": t.transaction_type,
                    "amount": t.amount,
                    "currency": t.currency,
                    "status": t.status,
                    "description": t.description
                }
                for t in txs
            ]
        }


reporting_engine = ReportingEngine()
