"""Configuration Management for FinXCore Platform."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FinXCore Digital Banking Super Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "finxcore-super-production-secret-key-at-least-32-chars-2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours for seamless demo & development
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./finxcore_banking.db")

    # Cors
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
        "*"
    ]

    # Rails and Defaults
    UPI_VPA_SUFFIX: str = "@finx"
    DEFAULT_CURRENCY: str = "INR"
    COUNTRY_CODE: str = "IND"
    ORGANIZATION_NAME: str = "FinXCore Global Banking Ltd."

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    class Config:
        case_sensitive = True
        extra = "allow"


settings = Settings()
