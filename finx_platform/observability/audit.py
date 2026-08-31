"""Immutable Audit Trail System."""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from sqlalchemy import Column, String, Text, DateTime
from finx_platform.common.database import Base
from finx_platform.common.base_model import generate_uuid, TimestampMixin
from finx_platform.observability.correlation import get_correlation_id, get_current_user_id


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    actor_id = Column(String(100), nullable=False, index=True)
    actor_role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(100), nullable=False, index=True)
    correlation_id = Column(String(100), nullable=False)
    ip_address = Column(String(50), default="127.0.0.1")
    user_agent = Column(String(255), default="FinXCore-Client/1.0")
    reason = Column(String(255), nullable=True)
    before_state = Column(Text, nullable=True)
    after_state = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)


class AuditService:
    @staticmethod
    def record(
        db,
        actor_id: str,
        actor_role: str,
        action: str,
        resource_type: str,
        resource_id: str,
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None,
        reason: Optional[str] = None,
        ip_address: str = "127.0.0.1",
        user_agent: str = "FinXCore-Client",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        log = AuditLog(
            actor_id=actor_id or get_current_user_id() or "system",
            actor_role=actor_role or "SYSTEM",
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            correlation_id=get_correlation_id(),
            ip_address=ip_address,
            user_agent=user_agent,
            reason=reason,
            before_state=json.dumps(before_state) if before_state else None,
            after_state=json.dumps(after_state) if after_state else None,
            metadata_json=json.dumps(metadata) if metadata else None
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log


audit_service = AuditService()
