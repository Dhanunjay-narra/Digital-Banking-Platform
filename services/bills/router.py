"""Bills & Recurring Payments API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.bills.schemas import BillPayRequest, BillResponse
from services.bills.service import bill_service

router = APIRouter(prefix="/bills", tags=["Bills & Utilities"])


@router.get("", response_model=List[BillResponse])
def get_my_bills(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return bill_service.get_or_seed_bills(db, customer.id)


@router.post("/pay", response_model=BillResponse)
def pay_bill(req: BillPayRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return bill_service.pay_bill(db, customer.id, req)
