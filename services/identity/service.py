"""Identity & IAM Business Logic Service."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from platform.security.password import hash_password, verify_password
from platform.security.jwt_handler import create_access_token, create_refresh_token, decode_token
from platform.security.mfa import mfa_service
from platform.common.exceptions import FinTechException, EntityNotFoundException
from services.identity.models import User, UserSession, UserDevice
from services.identity.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse


class IdentityService:
    @staticmethod
    def register_user(db: Session, req: UserRegisterRequest) -> User:
        existing = db.query(User).filter((User.email == req.email) | (User.phone_number == req.phone_number)).first()
        if existing:
            raise FinTechException("User with this email or phone already exists", code="USER_EXISTS", status_code=400)

        user = User(
            email=req.email,
            phone_number=req.phone_number,
            hashed_password=hash_password(req.password),
            first_name=req.first_name,
            last_name=req.last_name,
            role=req.role.upper(),
            is_active=True,
            is_verified=True,  # Auto-verified in development
            mfa_enabled=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, req: UserLoginRequest, ip: str = "127.0.0.1", user_agent: str = "FinXCore-Web") -> TokenResponse:
        user = db.query(User).filter(User.email == req.email).first()
        if not user or not verify_password(req.password, user.hashed_password):
            raise FinTechException("Invalid email or password", code="INVALID_CREDENTIALS", status_code=401)

        if not user.is_active:
            raise FinTechException("User account is disabled", code="USER_INACTIVE", status_code=403)

        # Register or update device
        if req.device_id:
            device = db.query(UserDevice).filter(UserDevice.user_id == user.id, UserDevice.device_id == req.device_id).first()
            if not device:
                device = UserDevice(
                    user_id=user.id,
                    device_id=req.device_id,
                    device_name=req.device_name or "Web Device",
                    device_type="WEB",
                    is_trusted=True
                )
                db.add(device)
            else:
                device.last_active_at = datetime.now(timezone.utc)
            db.commit()

        token_payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        # Record session
        session = UserSession(
            user_id=user.id,
            refresh_token_hash=hash_password(refresh_token[:20]),
            ip_address=ip,
            user_agent=user_agent,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(session)
        db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            mfa_required=user.mfa_enabled
        )

    @staticmethod
    def send_otp(identifier: str) -> str:
        return mfa_service.generate_otp(identifier)

    @staticmethod
    def verify_otp_and_login(db: Session, identifier: str, otp: str) -> TokenResponse:
        valid = mfa_service.verify_otp(identifier, otp)
        if not valid:
            raise FinTechException("Invalid or expired OTP", code="INVALID_OTP", status_code=400)

        user = db.query(User).filter((User.email == identifier) | (User.phone_number == identifier)).first()
        if not user:
            # Auto-create guest/sandbox user for easy passwordless testing
            name_part = identifier.split("@")[0] if "@" in identifier else identifier
            user = User(
                email=identifier if "@" in identifier else f"{identifier}@finxcore.com",
                phone_number=identifier if not "@" in identifier else "+919876543210",
                hashed_password=hash_password("Demo@12345"),
                first_name=name_part.capitalize(),
                last_name="User",
                role="CUSTOMER",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        token_payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return TokenResponse(
            access_token=create_access_token(token_payload),
            refresh_token=create_refresh_token(token_payload),
            user_id=user.id,
            email=user.email,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name
        )


identity_service = IdentityService()
