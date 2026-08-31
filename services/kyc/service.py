"""KYC Domain Service with Real & Simulator Logic."""

import re
from typing import Dict, Any
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, EntityNotFoundException
from services.kyc.models import KYCApplication, VerificationLog
from services.kyc.schemas import KYCSubmitRequest, PANVerifyRequest, BankVerifyRequest


class KYCService:
    @staticmethod
    def verify_pan_format(pan: str) -> bool:
        # Standard Indian PAN format: 5 letters, 4 digits, 1 letter
        pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        return bool(re.match(pattern, pan.upper()))

    @staticmethod
    def submit_kyc(db: Session, customer_id: str, req: KYCSubmitRequest) -> KYCApplication:
        pan_valid = KYCService.verify_pan_format(req.pan_number)
        if not pan_valid:
            raise FinTechException("Invalid PAN number format (expected e.g. ABCDE1234F)", code="INVALID_PAN", status_code=400)

        # Risk-based classification (CDD / EDD)
        risk_level = "LOW"
        if req.annual_income > 5000000.0:
            risk_level = "MEDIUM"
        if req.annual_income > 20000000.0:
            risk_level = "HIGH"

        kyc = db.query(KYCApplication).filter(KYCApplication.customer_id == customer_id).first()
        if not kyc:
            kyc = KYCApplication(
                customer_id=customer_id,
                status="VERIFIED",  # Auto-verified in platform simulator
                kyc_level="FULL_KYC",
                document_type=req.document_type,
                document_number=req.document_number,
                pan_verified=True,
                bank_verified=True,
                risk_level=risk_level,
                verified_by="AUTOMATED_RISK_ENGINE"
            )
            db.add(kyc)
        else:
            kyc.status = "VERIFIED"
            kyc.document_number = req.document_number
            kyc.pan_verified = True
            kyc.risk_level = risk_level

        db.commit()
        db.refresh(kyc)
        return kyc

    @staticmethod
    def verify_pan(db: Session, req: PANVerifyRequest) -> Dict[str, Any]:
        valid = KYCService.verify_pan_format(req.pan_number)
        return {
            "pan_number": req.pan_number.upper(),
            "is_valid": valid,
            "status": "ACTIVE" if valid else "INVALID",
            "name_match_score": 98.5 if valid else 0.0,
            "verified_via": "REGULATED_NSDL_SIMULATOR"
        }

    @staticmethod
    def verify_bank_account(db: Session, req: BankVerifyRequest) -> Dict[str, Any]:
        return {
            "account_number": req.account_number,
            "ifsc_code": req.ifsc_code.upper(),
            "bank_name": "FinX Core Partner Bank",
            "registered_name": req.beneficiary_name.upper(),
            "is_active": True,
            "penny_drop_status": "CREDIT_SUCCESS",
            "amount_credited": 1.00
        }


kyc_service = KYCService()
