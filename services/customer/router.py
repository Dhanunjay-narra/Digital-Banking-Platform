"""Customer API Endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.models import Customer
from services.customer.schemas import (
    CustomerCreate,
    CustomerResponse,
    Customer360Response,
    BeneficiaryCreate,
    NomineeCreate
)
from services.customer.service import customer_service

router = APIRouter(prefix="/customers", tags=["Customer Management"])


@router.get("/me")
def get_my_customer_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return customer_service.get_customer_360(db, customer.id)


@router.get("/{customer_id}/360")
def get_customer_360_view(customer_id: str, db: Session = Depends(get_db)):
    return customer_service.get_customer_360(db, customer_id)


@router.post("/beneficiaries")
def add_beneficiary(req: BeneficiaryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return customer_service.add_beneficiary(db, customer.id, req)


@router.get("/beneficiaries")
def list_beneficiaries(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return customer_service.get_beneficiaries(db, customer.id)


@router.post("/nominees")
def add_nominee(req: NomineeCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return customer_service.add_nominee(db, customer.id, req)
