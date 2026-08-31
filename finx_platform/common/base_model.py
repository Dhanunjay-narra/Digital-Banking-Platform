"""Base SQLAlchemy models and mixins."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_uuid() -> str:
    return str(uuid.uuid4())


class TimestampMixin:
    """Provides created_at, updated_at, and is_deleted audit fields."""
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
