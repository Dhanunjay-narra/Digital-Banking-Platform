"""Cards Management API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from platform.common.database import get_db
from services.identity.router import get_current_user
from services.identity.models import User
from services.customer.service import customer_service
from services.cards.schemas import (
    CardIssueRequest,
    CardPINSetRequest,
    CardControlsUpdateRequest,
    CardResponse,
    CardRevealResponse
)
from services.cards.service import card_service
from services.cards.models import PaymentCard

router = APIRouter(prefix="/cards", tags=["Card Platform"])


@router.get("", response_model=List[CardResponse])
def get_my_cards(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    cards = db.query(PaymentCard).filter(PaymentCard.customer_id == customer.id).all()
    if not cards:
        # Issue a default virtual RuPay card
        card = card_service.issue_card(db, customer.id, CardIssueRequest(
            card_type="VIRTUAL",
            card_network="RUPAY",
            cardholder_name=f"{user.first_name} {user.last_name}"
        ))
        return [card]
    return cards


@router.post("/issue", response_model=CardResponse)
def issue_new_card(req: CardIssueRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customer = customer_service.get_or_create_customer(db, user.id)
    return card_service.issue_card(db, customer.id, req)


@router.get("/{card_id}/reveal", response_model=CardRevealResponse)
def reveal_card_details(card_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return card_service.reveal_card(db, card_id)


@router.patch("/{card_id}/controls", response_model=CardResponse)
def update_card_controls(card_id: str, req: CardControlsUpdateRequest, db: Session = Depends(get_db)):
    return card_service.update_controls(db, card_id, req)


@router.post("/{card_id}/toggle-block", response_model=CardResponse)
def toggle_card_block(card_id: str, db: Session = Depends(get_db)):
    return card_service.toggle_block(db, card_id)
