"""Card Management Business Logic Service."""

import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from finx_platform.common.exceptions import FinTechException, EntityNotFoundException
from finx_platform.security.password import hash_password, verify_password
from finx_platform.security.crypto import encrypt_data, decrypt_data, mask_card_number
from services.cards.models import PaymentCard, CardType
from services.cards.schemas import CardIssueRequest, CardPINSetRequest, CardControlsUpdateRequest, CardRevealResponse


class CardService:
    @staticmethod
    def generate_luhn_card_number(network: str = "RUPAY") -> str:
        # Prefix based on network: RuPay=60/65, Visa=4, MasterCard=5
        prefix = "6521" if network == "RUPAY" else "4111" if network == "VISA" else "5200"
        digits = [int(x) for x in prefix]
        while len(digits) < 15:
            digits.append(random.randint(0, 9))

        # Luhn checksum calculation
        checksum = 0
        for idx, digit in enumerate(reversed(digits)):
            if idx % 2 == 0:
                doubled = digit * 2
                checksum += (doubled - 9) if doubled > 9 else doubled
            else:
                checksum += digit
        check_digit = (10 - (checksum % 10)) % 10
        digits.append(check_digit)
        return "".join(map(str, digits))

    @staticmethod
    def issue_card(db: Session, customer_id: str, req: CardIssueRequest) -> PaymentCard:
        card_num = CardService.generate_luhn_card_number(req.card_network)
        cvv = f"{random.randint(100, 999)}"
        exp_year = str(datetime.now(timezone.utc).year + 5)
        exp_month = "12"

        card = PaymentCard(
            customer_id=customer_id,
            card_number_masked=mask_card_number(card_num),
            card_number_encrypted=encrypt_data(card_num),
            card_type=req.card_type,
            card_network=req.card_network,
            expiry_month=exp_month,
            expiry_year=exp_year,
            cvv_encrypted=encrypt_data(cvv),
            cardholder_name=req.cardholder_name.upper(),
            pin_hash=hash_password(req.pin) if req.pin else hash_password("1234"),
            status="ACTIVE",
            online_enabled=True,
            atm_enabled=True,
            pos_enabled=True,
            contactless_enabled=True,
            international_enabled=False,
            daily_limit=50000.0
        )
        db.add(card)
        db.commit()
        db.refresh(card)
        return card

    @staticmethod
    def reveal_card(db: Session, card_id: str) -> CardRevealResponse:
        card = db.query(PaymentCard).filter(PaymentCard.id == card_id).first()
        if not card:
            raise EntityNotFoundException("PaymentCard", card_id)

        raw_num = decrypt_data(card.card_number_encrypted)
        raw_cvv = decrypt_data(card.cvv_encrypted)
        return CardRevealResponse(
            id=card.id,
            card_number=raw_num,
            cvv=raw_cvv,
            expiry=f"{card.expiry_month}/{card.expiry_year[-2:]}",
            cardholder_name=card.cardholder_name
        )

    @staticmethod
    def update_controls(db: Session, card_id: str, req: CardControlsUpdateRequest) -> PaymentCard:
        card = db.query(PaymentCard).filter(PaymentCard.id == card_id).first()
        if not card:
            raise EntityNotFoundException("PaymentCard", card_id)

        if req.online_enabled is not None:
            card.online_enabled = req.online_enabled
        if req.atm_enabled is not None:
            card.atm_enabled = req.atm_enabled
        if req.pos_enabled is not None:
            card.pos_enabled = req.pos_enabled
        if req.contactless_enabled is not None:
            card.contactless_enabled = req.contactless_enabled
        if req.international_enabled is not None:
            card.international_enabled = req.international_enabled
        if req.daily_limit is not None:
            card.daily_limit = req.daily_limit

        db.commit()
        db.refresh(card)
        return card

    @staticmethod
    def toggle_block(db: Session, card_id: str) -> PaymentCard:
        card = db.query(PaymentCard).filter(PaymentCard.id == card_id).first()
        if not card:
            raise EntityNotFoundException("PaymentCard", card_id)

        card.status = "BLOCKED" if card.status == "ACTIVE" else "ACTIVE"
        db.commit()
        db.refresh(card)
        return card


card_service = CardService()
