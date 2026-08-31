"""Investments & Wealth Management Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class AssetClass(str, Enum):
    MUTUAL_FUND = "MUTUAL_FUND"
    STOCK = "STOCK"
    ETF = "ETF"
    BOND = "BOND"
    FIXED_DEPOSIT = "FIXED_DEPOSIT"
    GOLD = "GOLD"


class PortfolioHolding(Base, TimestampMixin):
    __tablename__ = "portfolio_holdings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    asset_symbol = Column(String(50), nullable=False)
    asset_name = Column(String(150), nullable=False)
    asset_class = Column(String(30), default=AssetClass.MUTUAL_FUND.value, nullable=False)
    units = Column(Float, default=0.0, nullable=False)
    average_buy_price = Column(Float, default=0.0, nullable=False)
    current_market_price = Column(Float, default=0.0, nullable=False)
    invested_amount = Column(Float, default=0.0, nullable=False)
    current_value = Column(Float, default=0.0, nullable=False)
    unrealized_pnl = Column(Float, default=0.0, nullable=False)


class SIPPlan(Base, TimestampMixin):
    __tablename__ = "sip_plans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False, index=True)
    asset_symbol = Column(String(50), nullable=False)
    asset_name = Column(String(150), nullable=False)
    monthly_amount = Column(Float, nullable=False)
    sip_day = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
