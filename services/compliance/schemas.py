"""Compliance Pydantic Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SanctionsCheckRequest(BaseModel):
    full_name: str
    country: Optional[str] = "IND"


class SanctionMatchResponse(BaseModel):
    is_matched: bool
    confidence_score: float
    matched_entity: Optional[str] = None
    list_source: Optional[str] = None
    action_required: str = "ALLOW"  # ALLOW, BLOCK_AND_REPORT


class SARCreateRequest(BaseModel):
    customer_id: str
    suspicion_reason: str
    narrative: str
    involved_amount: float
