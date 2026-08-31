"""Digital Wallet API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.wallet.schemas import (
    WalletTopupRequest,
    WalletWithdrawRequest,
    WalletTransferRequest,
    WalletResponse,
    WalletTransactionResponse
)
from services.wallet.service import wallet_service
from services.wallet.models import DigitalWallet, WalletTransaction

router = APIRouter(prefix="/wallets", tags=["Digital Wallet"])


@router.get("/me", response_model=WalletResponse)
def get_my_wallet(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return wallet_service.get_or_create_wallet(db, customer.id)


@router.post("/topup", response_model=WalletResponse)
def top_up_wallet(req: WalletTopupRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return wallet_service.top_up_wallet(db, customer.id, req)


@router.post("/withdraw", response_model=WalletResponse)
def withdraw_wallet(req: WalletWithdrawRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return wallet_service.withdraw_to_bank(db, customer.id, req)


@router.get("/transactions", response_model=List[WalletTransactionResponse])
def get_wallet_transactions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    wallet = wallet_service.get_or_create_wallet(db, customer.id)
    return db.query(WalletTransaction).filter(WalletTransaction.wallet_id == wallet.id).order_by(WalletTransaction.created_at.desc()).limit(50).all()
