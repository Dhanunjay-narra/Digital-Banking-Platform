"""Customer Domain Database Models."""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from platform.common.database import Base
from platform.common.base_model import generate_uuid, TimestampMixin


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False, index=True)
    customer_segment = Column(String(50), default="RETAIL_STANDARD")  # RETAIL_STANDARD, PREMIUM, HNI, WEALTH
    customer_status = Column(String(50), default="ACTIVE")  # ACTIVE, DORMANT, SUSPENDED, BLOCKED
    pan_number = Column(String(20), nullable=True, index=True)
    national_id = Column(String(50), nullable=True)
    date_of_birth = Column(String(20), nullable=True)
    occupation = Column(String(100), nullable=True)
    annual_income = Column(Float, default=0.0)
    risk_rating = Column(String(20), default="LOW")  # LOW, MEDIUM, HIGH
    preferred_currency = Column(String(10), default="INR")
    preferred_language = Column(String(10), default="en")

    addresses = relationship("CustomerAddress", back_populates="customer", cascade="all, delete-orphan")
    beneficiaries = relationship("CustomerBeneficiary", back_populates="customer", cascade="all, delete-orphan")
    nominees = relationship("CustomerNominee", back_populates="customer", cascade="all, delete-orphan")


class CustomerAddress(Base, TimestampMixin):
    __tablename__ = "customer_addresses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    address_type = Column(String(50), default="CURRENT")  # PERMANENT, CURRENT, OFFICE
    street_line1 = Column(String(255), nullable=False)
    street_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(50), default="India")
    is_primary = Column(Boolean, default=True)

    customer = relationship("Customer", back_populates="addresses")


class CustomerBeneficiary(Base, TimestampMixin):
    __tablename__ = "customer_beneficiaries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    vpa_address = Column(String(100), nullable=True)
    bank_name = Column(String(100), nullable=True)
    transfer_type = Column(String(30), default="INTERNAL")  # INTERNAL, NEFT, IMPS, RTGS, UPI
    daily_limit = Column(Float, default=100000.0)
    is_verified = Column(Boolean, default=True)

    customer = relationship("Customer", back_populates="beneficiaries")


class CustomerNominee(Base, TimestampMixin):
    __tablename__ = "customer_nominees"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    relationship_type = Column(String(50), nullable=False)  # SPOUSE, CHILD, PARENT, SIBLING
    date_of_birth = Column(String(20), nullable=True)
    share_percentage = Column(Float, default=100.0)
    contact_number = Column(String(30), nullable=True)

    customer = relationship("Customer", back_populates="nominees")
