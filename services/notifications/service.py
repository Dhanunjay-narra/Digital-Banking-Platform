"""Centralized Multi-Channel Notification Service."""

from sqlalchemy.orm import Session
from finx_platform.observability.logger import get_logger
from services.notifications.models import NotificationLog
from services.notifications.schemas import NotificationSendRequest

logger = get_logger("notification.service")


class NotificationService:
    @staticmethod
    def send(db: Session, req: NotificationSendRequest) -> NotificationLog:
        log = NotificationLog(
            recipient=req.recipient,
            channel=req.channel,
            title=req.title,
            body=req.body,
            status="DELIVERED",
            is_read=False
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        logger.info(f"Notification sent via {req.channel} to {req.recipient}: {req.title}")
        return log


notification_service = NotificationService()
