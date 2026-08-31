"""Notifications Platform Database Models."""

from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin


class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    IN_APP = "IN_APP"


class NotificationLog(Base, TimestampMixin):
    __tablename__ = "notification_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    recipient = Column(String(150), nullable=False, index=True)
    channel = Column(String(30), default=NotificationChannel.IN_APP.value, nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(30), default="DELIVERED")  # SENT, DELIVERED, FAILED, READ
    is_read = Column(Boolean, default=False)
