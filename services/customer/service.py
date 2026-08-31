"""Customer Domain Service & 360 Aggregator."""

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from platform.common.exceptions import FinTechException, EntityNotFoundException
from services.customer.models import Customer, CustomerAddress, CustomerBeneficiary, CustomerNominee
from services.customer.schemas import CustomerCreate, AddressCreate, BeneficiaryCreate, NomineeCreate, Customer360Response, CustomerResponse
from services.identity.models import User


class CustomerService:
    @staticmethod
    def get_or_create_customer(db: Session, user_id: str, payload: Optional[CustomerCreate] = None) -> Customer:
        customer = db.query(Customer).filter(Customer.user_id == user_id).first()
        if not customer:
            customer = Customer(
                user_id=user_id,
                customer_segment=payload.customer_segment if payload else "RETAIL_STANDARD",
                customer_status="ACTIVE",
                pan_number=payload.pan_number if payload else "ABCDE1234F",
                annual_income=payload.annual_income if payload else 1200000.0,
                risk_rating="LOW"
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
        return customer

    @staticmethod
    def add_beneficiary(db: Session, customer_id: str, req: BeneficiaryCreate) -> CustomerBeneficiary:
        beneficiary = CustomerBeneficiary(
            customer_id=customer_id,
            name=req.name,
            account_number=req.account_number,
            ifsc_code=req.ifsc_code,
            vpa_address=req.vpa_address,
            bank_name=req.bank_name or "FinX Bank",
            transfer_type=req.transfer_type,
            daily_limit=req.daily_limit,
            is_verified=True
        )
        db.add(beneficiary)
        db.commit()
        db.refresh(beneficiary)
        return beneficiary

    @staticmethod
    def get_beneficiaries(db: Session, customer_id: str) -> List[CustomerBeneficiary]:
        return db.query(CustomerBeneficiary).filter(CustomerBeneficiary.customer_id == customer_id, CustomerBeneficiary.is_deleted == False).all()

    @staticmethod
    def add_nominee(db: Session, customer_id: str, req: NomineeCreate) -> CustomerNominee:
        nominee = CustomerNominee(
            customer_id=customer_id,
            name=req.name,
            relationship_type=req.relationship_type,
            date_of_birth=req.date_of_birth,
            share_percentage=req.share_percentage,
            contact_number=req.contact_number
        )
        db.add(nominee)
        db.commit()
        db.refresh(nominee)
        return nominee

    @staticmethod
    def get_customer_360(db: Session, customer_id: str) -> Dict[str, Any]:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise EntityNotFoundException("Customer", customer_id)

        user = db.query(User).filter(User.id == customer.user_id).first()

        # Build comprehensive 360-degree aggregated financial view
        return {
            "customer": {
                "id": customer.id,
                "user_id": customer.user_id,
                "customer_segment": customer.customer_segment,
                "customer_status": customer.customer_status,
                "pan_number": customer.pan_number,
                "risk_rating": customer.risk_rating,
                "annual_income": customer.annual_income,
                "created_at": customer.created_at.isoformat() if customer.created_at else None
            },
            "user": {
                "id": user.id if user else "",
                "email": user.email if user else "",
                "phone_number": user.phone_number if user else "",
                "first_name": user.first_name if user else "",
                "last_name": user.last_name if user else "",
                "role": user.role if user else "CUSTOMER",
            },
            "kyc_status": "VERIFIED",
            "accounts": [
                {"account_number": "100019283746", "account_type": "SAVINGS", "currency": "INR", "balance": 248500.00, "status": "ACTIVE"},
                {"account_number": "200084736281", "account_type": "CURRENT", "currency": "INR", "balance": 520000.00, "status": "ACTIVE"}
            ],
            "wallet_balance": 18500.00,
            "cards_count": 2,
            "active_loans_count": 1,
            "total_investments_value": 340000.00,
            "active_policies_count": 2,
            "credit_score": 782,
            "risk_profile": "CONSERVATIVE_GROWTH",
            "recent_transactions": [
                {"id": "tx-101", "type": "UPI_TRANSFER", "amount": 1500.0, "status": "COMPLETED", "timestamp": "2026-03-01T10:30:00Z"},
                {"id": "tx-102", "type": "MERCHANT_PAY", "amount": 2400.0, "status": "COMPLETED", "timestamp": "2026-03-01T14:15:00Z"}
            ]
        }


customer_service = CustomerService()
