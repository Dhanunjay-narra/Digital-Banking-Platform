"""Merchant Payment Gateway Processing Service."""

import json
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, EntityNotFoundException
from services.payments.models import PaymentOrder, PaymentRefund, PaymentStatus
from services.payments.schemas import PaymentOrderCreate, PaymentCaptureRequest, PaymentRefundRequest
from services.ledger.service import ledger_service
from services.ledger.schemas import JournalEntryCreate, PostingCreate


class PaymentGatewayService:
    @staticmethod
    def create_order(db: Session, req: PaymentOrderCreate) -> PaymentOrder:
        order_id = f"order_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
        order = PaymentOrder(
            order_id=order_id,
            merchant_id=req.merchant_id or "merch_demo_101",
            amount=req.amount,
            currency=req.currency,
            receipt=req.receipt or f"REC-{uuid.uuid4().hex[:6].upper()}",
            status=PaymentStatus.CREATED.value,
            customer_email=req.customer_email,
            customer_phone=req.customer_phone,
            notes_json=json.dumps(req.notes) if req.notes else None
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def capture_payment(db: Session, req: PaymentCaptureRequest) -> PaymentOrder:
        order = db.query(PaymentOrder).filter(PaymentOrder.order_id == req.order_id).first()
        if not order:
            raise EntityNotFoundException("PaymentOrder", req.order_id)

        order.status = PaymentStatus.CAPTURED.value
        order.amount_captured = req.amount
        order.payment_method = req.payment_method

        # Calculate merchant fee (e.g. 1.8% MDR)
        mdr_fee = round(req.amount * 0.018, 2)
        merchant_net = round(req.amount - mdr_fee, 2)

        # Authoritative Double-entry Ledger posting:
        # Debit Settlement Clearing (1010) ₹Amount
        # Credit Merchant Settlement Payable (2030) ₹Net
        # Credit Payment Processing Fee Revenue (4000) ₹MDR
        ledger_service.post_journal_entry(db, JournalEntryCreate(
            transaction_id=order.order_id,
            description=f"Payment Gateway Capture: {order.order_id} via {req.payment_method}",
            currency="INR",
            postings=[
                PostingCreate(account_code="1010", entry_type="DEBIT", amount=req.amount, description="Clearing Inflow"),
                PostingCreate(account_code="2030", entry_type="CREDIT", amount=merchant_net, description="Merchant Payable"),
                PostingCreate(account_code="4000", entry_type="CREDIT", amount=mdr_fee, description="MDR Platform Fee Revenue")
            ]
        ))

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def refund_payment(db: Session, req: PaymentRefundRequest) -> PaymentRefund:
        order = db.query(PaymentOrder).filter(PaymentOrder.order_id == req.order_id).first()
        if not order:
            raise EntityNotFoundException("PaymentOrder", req.order_id)

        if req.amount > (order.amount_captured - order.amount_refunded):
            raise FinTechException("Refund amount exceeds remaining captured balance", code="EXCESS_REFUND", status_code=400)

        refund_id = f"rfnd_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
        refund = PaymentRefund(
            refund_id=refund_id,
            order_id=order.id,
            amount=req.amount,
            currency=order.currency,
            status="PROCESSED",
            reason=req.reason
        )
        db.add(refund)

        order.amount_refunded += req.amount
        if order.amount_refunded >= order.amount_captured:
            order.status = PaymentStatus.REFUNDED.value
        else:
            order.status = PaymentStatus.PARTIALLY_REFUNDED.value

        # Reversal posting on Ledger
        ledger_service.post_journal_entry(db, JournalEntryCreate(
            transaction_id=refund_id,
            description=f"Gateway Refund for {order.order_id}",
            currency="INR",
            postings=[
                PostingCreate(account_code="2030", entry_type="DEBIT", amount=req.amount, description="Merchant Payable Debit"),
                PostingCreate(account_code="1010", entry_type="CREDIT", amount=req.amount, description="Clearing Outflow")
            ]
        ))

        db.commit()
        db.refresh(refund)
        return refund


payment_gateway_service = PaymentGatewayService()
