"""Bank Transfers API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.transfers.schemas import TransferInitiateRequest, TransferResponse
from services.transfers.service import transfer_service
from services.transfers.models import BankTransfer

router = APIRouter(prefix="/transfers", tags=["Bank Transfers"])


@router.post("/execute", response_model=TransferResponse)
def execute_transfer(req: TransferInitiateRequest, db: Session = Depends(get_db)):
    return transfer_service.execute_transfer(db, req)


@router.get("/history", response_model=List[TransferResponse])
def get_transfers_history(db: Session = Depends(get_db)):
    return db.query(BankTransfer).order_by(BankTransfer.created_at.desc()).limit(50).all()
