"""Banking Accounts API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.accounts.schemas import AccountCreateRequest, AccountResponse, AccountFreezeRequest
from services.accounts.service import account_service
from services.accounts.models import BankAccount

router = APIRouter(prefix="/accounts", tags=["Banking Accounts"])


@router.get("", response_model=List[AccountResponse])
def get_my_accounts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    accounts = db.query(BankAccount).filter(BankAccount.customer_id == customer.id).all()
    if not accounts:
        # Open a default savings account for seamless onboard
        acc = account_service.open_account(db, customer.id, AccountCreateRequest(account_type="SAVINGS", initial_deposit=50000.0))
        return [acc]
    return accounts


@router.post("", response_model=AccountResponse)
def open_new_account(req: AccountCreateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return account_service.open_account(db, customer.id, req)


@router.post("/freeze", response_model=AccountResponse)
def freeze_account(req: AccountFreezeRequest, db: Session = Depends(get_db)):
    return account_service.freeze_account(db, req.account_number, req.reason)


@router.post("/unfreeze", response_model=AccountResponse)
def unfreeze_account(req: AccountFreezeRequest, db: Session = Depends(get_db)):
    return account_service.unfreeze_account(db, req.account_number)
