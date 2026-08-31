"""UPI Rail Simulator Logic with QR Code & Real-Time Settlement."""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, EntityNotFoundException, InsufficientFundsException
from platform.security.password import hash_password, verify_password
from services.upi.models import UPIProfile, UPICollectRequest
from services.upi.schemas import VPARegisterRequest, UPISendRequest, UPICollectCreateRequest, QRCodeGenerateRequest, UPITransactionResponse
from services.accounts.models import BankAccount
from services.transactions.service import transaction_engine
from services.transactions.schemas import TransactionInitiateRequest


class UPIService:
    @staticmethod
    def get_or_create_profile(db: Session, customer_id: str, account_number: str = "100019283746") -> UPIProfile:
        profile = db.query(UPIProfile).filter(UPIProfile.customer_id == customer_id).first()
        if not profile:
            vpa = f"user.{customer_id[:6]}@finx"
            qr_uri = f"upi://pay?pa={vpa}&pn=FinXCustomer&cu=INR"
            profile = UPIProfile(
                customer_id=customer_id,
                vpa_address=vpa,
                linked_account_number=account_number,
                upi_pin_hash=hash_password("1234"),
                daily_limit=100000.0,
                is_active=True,
                qr_payload=qr_uri
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile

    @staticmethod
    def send_money(db: Session, customer_id: str, req: UPISendRequest) -> UPITransactionResponse:
        payer = UPIService.get_or_create_profile(db, customer_id)
        payee = db.query(UPIProfile).filter(UPIProfile.vpa_address == req.recipient_vpa).first()

        payer_acc_num = payer.linked_account_number
        payee_acc_num = payee.linked_account_number if payee else "200084736281"  # Fallback merchant/clearing account

        tx = transaction_engine.execute_transaction(db, TransactionInitiateRequest(
            source_account=payer_acc_num,
            destination_account=payee_acc_num,
            amount=req.amount,
            currency="INR",
            transaction_type="UPI_PAYMENT",
            channel="UPI",
            description=f"UPI Payment to {req.recipient_vpa}: {req.remarks}",
            metadata={"payer_vpa": payer.vpa_address, "payee_vpa": req.recipient_vpa}
        ))

        return UPITransactionResponse(
            success=True,
            transaction_id=tx.id,
            reference_number=tx.transaction_reference,
            payer_vpa=payer.vpa_address,
            payee_vpa=req.recipient_vpa,
            amount=req.amount,
            status=tx.status,
            timestamp=datetime.now(timezone.utc)
        )

    @staticmethod
    def generate_qr(db: Session, customer_id: str, req: QRCodeGenerateRequest) -> Dict[str, Any]:
        profile = UPIService.get_or_create_profile(db, customer_id)
        amt_param = f"&am={req.amount:.2f}" if req.amount else ""
        note_param = f"&tn={req.note}" if req.note else ""
        upi_url = f"upi://pay?pa={profile.vpa_address}&pn=FinXCustomer{amt_param}{note_param}&cu=INR"

        return {
            "vpa": profile.vpa_address,
            "amount": req.amount,
            "qr_payload": upi_url,
            "qr_type": "DYNAMIC" if req.amount else "STATIC",
            "format": "UPI_DEEP_LINK"
        }

    @staticmethod
    def create_collect_request(db: Session, customer_id: str, req: UPICollectCreateRequest) -> UPICollectRequest:
        profile = UPIService.get_or_create_profile(db, customer_id)
        collect = UPICollectRequest(
            requester_vpa=profile.vpa_address,
            payer_vpa=req.payer_vpa,
            amount=req.amount,
            currency="INR",
            remarks=req.remarks,
            status="PENDING"
        )
        db.add(collect)
        db.commit()
        db.refresh(collect)
        return collect


upi_service = UPIService()
