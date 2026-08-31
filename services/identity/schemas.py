"""Identity & IAM Pydantic Schemas."""

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserRegisterRequest(BaseModel):
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    first_name: str
    last_name: str
    role: str = "CUSTOMER"


class UserLoginRequest(BaseModel):
    email: str
    password: str
    device_id: Optional[str] = "web-default-device"
    device_name: Optional[str] = "Chrome Browser"


class OTPRequest(BaseModel):
    identifier: str  # Email or Phone


class OTPVerifyRequest(BaseModel):
    identifier: str
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str
    first_name: str
    last_name: str
    mfa_required: bool = False


class UserResponse(BaseModel):
    id: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    is_verified: bool
    mfa_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceResponse(BaseModel):
    id: str
    device_id: str
    device_name: str
    device_type: str
    is_trusted: bool
    last_active_at: datetime

    class Config:
        from_attributes = True
