"""Notifications API Endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.notifications.schemas import NotificationSendRequest, NotificationResponse
from services.notifications.service import notification_service
from services.notifications.models import NotificationLog

router = APIRouter(prefix="/notifications", tags=["Notification Platform"])


@router.post("/send", response_model=NotificationResponse)
def send_notification(req: NotificationSendRequest, db: Session = Depends(get_db)):
    return notification_service.send(db, req)


@router.get("", response_model=List[NotificationResponse])
def get_notifications(recipient: str = "customer@finxcore.com", db: Session = Depends(get_db)):
    logs = db.query(NotificationLog).filter(NotificationLog.recipient == recipient).order_by(NotificationLog.created_at.desc()).limit(20).all()
    if not logs:
        n1 = notification_service.send(db, NotificationSendRequest(
            recipient=recipient,
            channel="IN_APP",
            title="Welcome to FinXCore!",
            body="Your high-performance digital banking account is active. Explore UPI, Cards, Loans, and Investments."
        ))
        n2 = notification_service.send(db, NotificationSendRequest(
            recipient=recipient,
            channel="SMS",
            title="Security Alert: Device Trusted",
            body="A new Chrome Web session has been registered successfully."
        ))
        return [n1, n2]
    return logs
