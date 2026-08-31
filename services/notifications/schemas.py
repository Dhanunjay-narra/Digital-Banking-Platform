"""Notification Pydantic Schemas."""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class NotificationSendRequest(BaseModel):
    recipient: str
    channel: str = "IN_APP"
    title: str
    body: str


class NotificationResponse(BaseModel):
    id: str
    recipient: str
    channel: str
    title: str
    body: str
    status: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
