"""AML & Regulatory Compliance Database Models."""

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class SanctionEntry(Base, TimestampMixin):
    __tablename__ = "sanction_entries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    full_name = Column(String(200), index=True, nullable=False)
    aliases = Column(String(255), nullable=True)
    list_source = Column(String(100), default="UN_OFAC_PEP")  # UN_SANCTIONS, OFAC_SDN, PEP_GLOBAL
    country = Column(String(100), nullable=True)
    risk_category = Column(String(100), default="SANCTIONED_INDIVIDUAL")


class SARReport(Base, TimestampMixin):
    """Suspicious Activity Report (SAR) for FIU / Regulators."""
    __tablename__ = "sar_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sar_reference = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(String(36), nullable=False, index=True)
    suspicion_reason = Column(String(255), nullable=False)
    narrative = Column(Text, nullable=False)
    involved_amount = Column(Float, nullable=False)
    status = Column(String(30), default="DRAFT")  # DRAFT, SUBMITTED_TO_FIU, ARCHIVED
    filed_by = Column(String(100), nullable=False)
