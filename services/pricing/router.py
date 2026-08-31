"""Pricing & Fees API Endpoints."""

from fastapi import APIRouter, Query
from services.pricing.service import pricing_engine

router = APIRouter(prefix="/pricing", tags=["Pricing & Fees Engine"])


@router.get("/calculate")
def calculate_fee(
    service_type: str = Query("MERCHANT_MDR"),
    amount: float = Query(10000.0),
    customer_segment: str = Query("RETAIL_STANDARD")
):
    return pricing_engine.calculate_fee(service_type, amount, customer_segment)
