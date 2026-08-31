"""Bills & Utilities Management Business Logic."""

from datetime import datetime, timedelta, timezone
from typing import List
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, EntityNotFoundException, InsufficientFundsException
from services.bills.models import CustomerBill, BillerCategory
from services.bills.schemas import BillPayRequest
from services.accounts.models import BankAccount


class BillService:
    @staticmethod
    def get_or_seed_bills(db: Session, customer_id: str) -> List[CustomerBill]:
        bills = db.query(CustomerBill).filter(CustomerBill.customer_id == customer_id).all()
        if not bills:
            now = datetime.now(timezone.utc)
            samples = [
                ("Bescom Electricity", BillerCategory.ELECTRICITY.value, "BES10928374", 2450.0, now + timedelta(days=12)),
                ("Airtel Fiber Broadband", BillerCategory.BROADBAND.value, "0804928374", 1179.0, now + timedelta(days=5)),
                ("Tata Play DTH", BillerCategory.DTH.value, "TP88374628", 499.0, now + timedelta(days=18)),
                ("Indane LPG Cylinder", BillerCategory.UTILITIES_BILLS.value if hasattr(BillerCategory, 'UTILITIES_BILLS') else BillerCategory.ELECTRICITY.value, "LPG992837", 850.0, now + timedelta(days=22))
            ]
            for b_name, b_cat, c_num, amt, d_date in samples:
                bill = CustomerBill(
                    customer_id=customer_id,
                    biller_name=b_name,
                    biller_category=b_cat,
                    consumer_number=c_num,
                    amount=amt,
                    due_date=d_date,
                    status="UNPAID"
                )
                db.add(bill)
            db.commit()
            bills = db.query(CustomerBill).filter(CustomerBill.customer_id == customer_id).all()
        return bills

    @staticmethod
    def pay_bill(db: Session, customer_id: str, req: BillPayRequest) -> CustomerBill:
        bill = db.query(CustomerBill).filter(CustomerBill.id == req.bill_id, CustomerBill.customer_id == customer_id).first()
        if not bill:
            raise EntityNotFoundException("CustomerBill", req.bill_id)

        acc = db.query(BankAccount).filter(BankAccount.account_number == req.source_account_number).first()
        if acc:
            if acc.available_balance < bill.amount:
                raise InsufficientFundsException("Insufficient funds in bank account to pay bill.")
            acc.available_balance -= bill.amount

        bill.status = "PAID"
        bill.paid_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(bill)
        return bill


bill_service = BillService()
