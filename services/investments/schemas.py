"""Investments Pydantic Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class InvestmentOrderRequest(BaseModel):
    asset_symbol: str
    asset_name: str
    asset_class: str = "MUTUAL_FUND"
    order_type: str = Field("BUY", pattern="^(BUY|SELL)$")
    amount: float = Field(..., gt=100)
    source_account_number: Optional[str] = "100019283746"


class SIPCreateRequest(BaseModel):
    asset_symbol: str
    asset_name: str
    monthly_amount: float = Field(..., gt=500)
    sip_day: int = Field(5, ge=1, le=28)


class HoldingResponse(BaseModel):
    id: str
    asset_symbol: str
    asset_name: str
    asset_class: str
    units: float
    average_buy_price: float
    current_market_price: float
    invested_amount: float
    current_value: float
    unrealized_pnl: float

    class Config:
        from_attributes = True


class PortfolioSummaryResponse(BaseModel):
    total_invested: float
    current_value: float
    total_pnl: float
    total_pnl_percentage: float
    holdings: List[HoldingResponse]
