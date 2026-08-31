"""Identity & Authentication API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from platform.common.database import get_db
from platform.security.jwt_handler import decode_token
from platform.common.exceptions import FinTechException
from services.identity.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    OTPRequest,
    OTPVerifyRequest,
    DeviceResponse
)
from services.identity.service import identity_service
from services.identity.models import User, UserDevice

router = APIRouter(prefix="/auth", tags=["Identity & IAM"])


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise FinTechException("Missing or invalid Authorization header", code="UNAUTHORIZED", status_code=401)
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise FinTechException("User not found or inactive", code="UNAUTHORIZED", status_code=401)
    return user


@router.post("/register", response_model=UserResponse)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    return identity_service.register_user(db, req)


@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("User-Agent", "FinXCore-Client")
    return identity_service.authenticate_user(db, req, ip=client_ip, user_agent=ua)


@router.post("/otp/send")
def send_otp(req: OTPRequest):
    otp = identity_service.send_otp(req.identifier)
    return {"success": True, "message": "OTP sent successfully", "demo_otp": otp}


@router.post("/otp/verify", response_model=TokenResponse)
def verify_otp(req: OTPVerifyRequest, db: Session = Depends(get_db)):
    return identity_service.verify_otp_and_login(db, req.identifier, req.otp)


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.get("/devices", response_model=List[DeviceResponse])
def get_devices(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserDevice).filter(UserDevice.user_id == user.id).all()
