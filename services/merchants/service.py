"""Merchant Management & Settlement Business Logic."""

import uuid
import random
from datetime import datetime, timezone
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, EntityNotFoundException
from services.merchants.models import MerchantProfile, MerchantSettlement
from services.merchants.schemas import MerchantCreateRequest
from services.ledger.service import ledger_service
from services.ledger.schemas import JournalEntryCreate, PostingCreate


class MerchantService:
    @staticmethod
    def get_or_seed_merchant(db: Session, merchant_code: str = "merch_demo_101") -> MerchantProfile:
        merch = db.query(MerchantProfile).filter(MerchantProfile.merchant_code == merchant_code).first()
        if not merch:
            merch = MerchantProfile(
                merchant_code=merchant_code,
                business_name="NexGen Retail Enterprises Ltd.",
                business_type="ECOMMERCE",
                contact_email="billing@nexgenretail.com",
                contact_phone="+919876543210",
                settlement_account_number="200084736281",
                settlement_ifsc="FINX0001001",
                mdr_rate_percent=1.8,
                status="ACTIVE",
                api_key=f"key_live_finx_{uuid.uuid4().hex[:16]}",
                vpa_address="nexgen.pay@finx"
            )
            db.add(merch)
            db.commit()
            db.refresh(merch)
        return merch

    @staticmethod
    def create_merchant(db: Session, req: MerchantCreateRequest) -> MerchantProfile:
        code = f"merch_{uuid.uuid4().hex[:8]}"
        merch = MerchantProfile(
            merchant_code=code,
            business_name=req.business_name,
            business_type=req.business_type,
            contact_email=req.contact_email,
            contact_phone=req.contact_phone,
            settlement_account_number=req.settlement_account_number,
            settlement_ifsc=req.settlement_ifsc or "FINX0001001",
            mdr_rate_percent=1.8,
            status="ACTIVE",
            api_key=f"key_live_finx_{uuid.uuid4().hex[:16]}",
            vpa_address=f"{req.business_name.lower().replace(' ', '')[:10]}@finx"
        )
        db.add(merch)
        db.commit()
        db.refresh(merch)
        return merch

    @staticmethod
    def trigger_settlement(db: Session, merchant_id: str, gross_amount: float) -> MerchantSettlement:
        merch = db.query(MerchantProfile).filter(MerchantProfile.id == merchant_id).first()
        if not merch:
            raise EntityNotFoundException("Merchant", merchant_id)

        fee = round(gross_amount * (merch.mdr_rate_percent / 100), 2)
        net_settled = round(gross_amount - fee, 2)
        utr = f"SETTL{datetime.now(timezone.utc).strftime('%Y%m%d')}{random.randint(100000, 999999)}"

        settlement = MerchantSettlement(
            settlement_ref=f"SET-{uuid.uuid4().hex[:8].upper()}",
            merchant_id=merchant_id,
            gross_volume=gross_amount,
            fee_deducted=fee,
            net_settled_amount=net_settled,
            status="SETTLED",
            utr_number=utr
        )
        db.add(settlement)

        # Ledger settlement:
        # Debit Merchant Settlement Payable (2030) ₹Net
        # Credit Central Bank Vault (1000) ₹Net
        ledger_service.post_journal_entry(db, JournalEntryCreate(
            transaction_id=settlement.settlement_ref,
            description=f"Batch Merchant Settlement to {merch.business_name}",
            currency="INR",
            postings=[
                PostingCreate(account_code="2030", entry_type="DEBIT", amount=net_settled, description="Merchant Payable Clearance"),
                PostingCreate(account_code="1000", entry_type="CREDIT", amount=net_settled, description="Settlement Outflow")
            ]
        ))

        db.commit()
        db.refresh(settlement)
        return settlement


merchant_service = MerchantService()
