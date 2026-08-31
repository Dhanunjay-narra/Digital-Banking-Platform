"""KYC Domain Database Models."""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class KYCApplication(Base, TimestampMixin):
    __tablename__ = "kyc_applications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    status = Column(String(50), default="SUBMITTED")  # PENDING, SUBMITTED, IN_REVIEW, VERIFIED, REJECTED
    kyc_level = Column(String(30), default="FULL_KYC")  # MIN_KYC, FULL_KYC, VIDEO_KYC
    document_type = Column(String(50), default="AADHAAR")  # PAN, AADHAAR, PASSPORT, VOTER_ID, DRIVING_LICENSE
    document_number = Column(String(100), nullable=False)
    pan_verified = Column(Boolean, default=False)
    bank_verified = Column(Boolean, default=False)
    risk_level = Column(String(30), default="LOW")  # LOW, MEDIUM, HIGH (Enhanced Due Diligence needed)
    verified_by = Column(String(100), nullable=True)
    rejection_reason = Column(Text, nullable=True)


class VerificationLog(Base, TimestampMixin):
    __tablename__ = "verification_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    kyc_id = Column(String(36), ForeignKey("kyc_applications.id"), nullable=False, index=True)
    check_type = Column(String(50), nullable=False)  # PAN_CHECK, AADHAAR_CHECK, PENNY_DROP, SANCTION_SCREEN
    provider = Column(String(100), default="REGULATED_KYC_SIMULATOR")
    is_success = Column(Boolean, default=True)
    response_payload = Column(Text, nullable=True)
